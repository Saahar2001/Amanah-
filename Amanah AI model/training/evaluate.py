from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import sys

from data.models import DriftLabel, Severity, TRAINABLE_DRIFT_LABELS_V0
from training.metrics import compute_drift_metrics


def write_evaluation_report(metrics: dict, output_dir: str | Path) -> tuple[Path, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "metrics.json"
    md_path = out / "EVALUATION.md"
    json_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    lines = ["# AMANAH Evaluation", "", "> Generated only from measured inputs; no metric is fabricated.", ""]
    for key, value in metrics.items():
        if isinstance(value, (str, int, float)):
            lines.append(f"- **{key}:** {value}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def _finding_label(finding) -> str:
    if isinstance(finding, dict):
        value = finding.get("label")
    else:
        value = getattr(finding, "label", None)
    return getattr(value, "value", value)


def evaluate_rows(rows: list[dict], predictor, label_names: list[str] | None = None, batch_size: int | None = None) -> dict:
    if label_names is None:
        cfg = getattr(predictor, "_config", None)
        label_names = list(cfg.get("drift_labels", [])) if isinstance(cfg, dict) else []
    if not label_names:
        label_names = [x.value for x in TRAINABLE_DRIFT_LABELS_V0]

    labels = [DriftLabel(name) for name in label_names]
    label_index = {label.value: i for i, label in enumerate(labels)}
    sev_index = {severity.value: i for i, severity in enumerate(Severity)}

    y_true_rows: list[list[int]] = []
    y_pred_rows: list[list[int]] = []
    severity_true_rows: list[int] = []
    severity_pred_rows: list[int] = []
    abstained_rows = 0
    overlength_abstentions = 0
    total_critical_rows = sum(row["severity"] == Severity.S3.value for row in rows)
    scored_critical_rows = 0

    total_rows = len(rows)
    if batch_size is None:
        batch_size = 16 if getattr(predictor, '_device', 'cpu') == 'cuda' else 4
    print(
        f"Evaluation inference device: {getattr(predictor, '_device', 'unknown')} | batch_size={batch_size}",
        file=sys.stderr,
        flush=True,
    )

    for start_idx in range(0, total_rows, batch_size):
        batch = rows[start_idx:start_idx + batch_size]
        pairs = [(row["source_ar"], row["candidate_en"]) for row in batch]
        if hasattr(predictor, "predict_batch"):
            results = predictor.predict_batch(pairs, batch_size=batch_size)
        else:
            results = [predictor.predict(source_ar, candidate_en) for source_ar, candidate_en in pairs]
        if len(results) != len(batch):
            raise RuntimeError("evaluation result count mismatch")

        for row, result in zip(batch, results):
            row_is_critical = row["severity"] == Severity.S3.value
            if not result.get("available"):
                error = str(result.get("error", "model unavailable"))
                if error.startswith("input_exceeds_model_context:"):
                    abstained_rows += 1
                    overlength_abstentions += 1
                    continue
                return {
                    "status": "model_unavailable",
                    "rows": len(y_true_rows),
                    "model_version": result.get("model_version", "unknown"),
                    "error": error,
                }

            truth = [0] * len(labels)
            for label in row["labels"]:
                truth[label_index[label]] = 1

            pred = [0] * len(labels)
            findings = result.get("findings", [])
            if findings:
                for finding in findings:
                    label = _finding_label(finding)
                    if label in label_index:
                        pred[label_index[label]] = 1
            else:
                pred[label_index[DriftLabel.FAITHFUL.value]] = 1

            predicted_severity = result.get("severity")
            if predicted_severity not in sev_index:
                predicted_severity = "S0" if not findings else max(
                    (
                        getattr(getattr(f, "severity", None), "value", None)
                        or (f.get("severity") if isinstance(f, dict) else "S0")
                        for f in findings
                    ),
                    key=lambda s: sev_index.get(s, 0),
                    default="S0",
                )

            y_true_rows.append(truth)
            y_pred_rows.append(pred)
            severity_true_rows.append(sev_index[row["severity"]])
            severity_pred_rows.append(sev_index[predicted_severity])
            if row_is_critical:
                scored_critical_rows += 1

        done=min(start_idx + len(batch), total_rows)
        if done == len(batch) or done % max(batch_size * 10, 160) == 0 or done == total_rows:
            print(f"Evaluation progress: {done}/{total_rows}", file=sys.stderr, flush=True)

    if not y_true_rows:
        return {
            "status": "no_scoreable_rows",
            "rows": len(rows),
            "model_version": getattr(predictor, "model_version", "unknown"),
            "abstained_rows": abstained_rows,
        }

    y_true = np.asarray(y_true_rows, dtype=int)
    y_pred = np.asarray(y_pred_rows, dtype=int)
    severity_true = np.asarray(severity_true_rows, dtype=int)
    severity_pred = np.asarray(severity_pred_rows, dtype=int)

    metrics = compute_drift_metrics(
        y_true,
        y_pred,
        severity_true,
        severity_pred,
        critical_mask=(severity_true == sev_index[Severity.S3.value]),
        faithful_index=label_index.get(DriftLabel.FAITHFUL.value),
    )
    scored_rows = len(y_true_rows)
    return {
        "status": "ok",
        "rows": total_rows,
        "scored_rows": scored_rows,
        "abstained_rows": abstained_rows,
        "overlength_abstentions": overlength_abstentions,
        "coverage": float(scored_rows / total_rows) if total_rows else 0.0,
        "abstention_rate": float(abstained_rows / total_rows) if total_rows else 0.0,
        "critical_coverage": float(scored_critical_rows / total_critical_rows) if total_critical_rows else 1.0,
        "model_version": getattr(predictor, "model_version", "unknown"),
        **metrics,
    }


def evaluate_checkpoint(*, checkpoint: str, test_path: str, output_dir: str) -> dict:
    from amanah_engine.classifier import ClassifierAdapter
    test = Path(test_path)
    if not test.exists(): raise FileNotFoundError(test)
    rows = [json.loads(line) for line in test.read_text(encoding="utf-8").splitlines() if line.strip()]
    predictor = ClassifierAdapter(checkpoint)
    metrics = evaluate_rows(rows, predictor, label_names=list(predictor._config.get("drift_labels", [])) if getattr(predictor, "_config", None) else None)
    write_evaluation_report(metrics, output_dir)
    return metrics


def main():
    p = argparse.ArgumentParser(); p.add_argument("--checkpoint", required=True); p.add_argument("--test", required=True); p.add_argument("--output", required=True)
    a = p.parse_args(); print(json.dumps(evaluate_checkpoint(checkpoint=a.checkpoint, test_path=a.test, output_dir=a.output)))


if __name__ == "__main__": main()
