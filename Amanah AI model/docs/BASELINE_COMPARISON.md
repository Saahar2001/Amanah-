# Baseline and Model Comparison Protocol

## Principle

A fair numerical comparison requires every model to be evaluated on the **same frozen test rows, label definitions, source context, and metric implementation**. This repository therefore separates measured AMANAH results from proposed comparison baselines.

No external-model score is fabricated or copied from an unrelated benchmark.

## AMANAH measured result

| System | Same AMANAH held-out split? | Macro F1 | Critical Drift Recall | Coverage |
|---|---|---:|---:|---:|
| AMANAH v0.2 | Yes | **95.26%** | **96.95%** | **98.53%** |

## Recommended baselines to run

1. **Base multilingual NLI encoder without AMANAH fine-tuning**
   - isolates the value of task-specific training;
   - use the same input serialization and test rows.

2. **Lexical/rule-only baseline**
   - isolates what deterministic heuristics can detect;
   - expected to be strong on narrow patterns and weak on paraphrase.

3. **RAG + general LLM baseline**
   - provide the same trusted references;
   - require structured labels;
   - evaluate repeated runs if the model is non-deterministic.

4. **General LLM without retrieval**
   - useful as a demonstration of the risk of unsupported reasoning;
   - should never receive privileged ground-truth labels.

5. **Alternative multilingual encoder (for example XLM-R)**
   - train on exactly the same train split;
   - calibrate on the same validation split;
   - score once on the frozen test split.

## Metrics that must be reported

- Macro F1
- per-label F1
- Critical Drift Recall
- False Safe Rate
- Coverage
- Critical Coverage
- Abstention Rate
- latency and memory footprint if operational efficiency is compared

## Qualitative architecture comparison

| Capability | AMANAH | RAG-only LLM | General LLM only | Rules only |
|---|---|---|---|---|
| Task-specific trained classifier | Yes | No | No | No |
| Trusted source grounding | Yes | Usually | Optional | Optional |
| Structured drift taxonomy | Yes | Prompt-dependent | Prompt-dependent | Limited |
| Deterministic high-risk guards | Yes | No | No | Yes |
| Explicit fail-closed abstention | Yes | Must be engineered | Must be engineered | Possible |
| Reproducible threshold calibration | Yes | Usually no | Usually no | N/A |
| Human-review state | Yes | Must be engineered | Must be engineered | Possible |

This table is a systems comparison, not a substitute for a numerical benchmark.

## Presentation guidance

Safe statement:
> “AMANAH achieved 95.26% Macro F1 on our frozen held-out semantic-drift benchmark. We compare competing architectures under the same test protocol before making numerical superiority claims.”

Avoid:
> “AMANAH is 95% more accurate than GPT / RAG / XLM-R.”

Such a statement is unsupported unless those systems are run on the same benchmark.
