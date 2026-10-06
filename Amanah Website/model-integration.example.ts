export interface AmanahInput {
  source_type: "quran";
  source_ar: string;
  candidate_en: string;
  ayah_id: string;
}

export interface AmanahResult {
  decision: "PASS" | "REVIEW" | "CRITICAL" | "ABSTAIN";
  integrity_score: number;
  severity: "S0" | "S1" | "S2" | "S3";
  confidence: number;
  drifts: Array<Record<string, unknown>>;
  needs_human_review: boolean;
  model_version: string;
  reference_status: string;
  notes: string[];
}

function unavailableResult(note: string): AmanahResult {
  return {
    decision: "ABSTAIN",
    integrity_score: 0,
    severity: "S0",
    confidence: 0,
    drifts: [],
    needs_human_review: true,
    model_version: "unavailable",
    reference_status: "unavailable",
    notes: [note],
  };
}

export async function analyzeWithAmanah(
  input: AmanahInput,
  env: { AMANAH_ML_URL: string; AMANAH_ML_TOKEN: string }
): Promise<AmanahResult> {
  if (!env.AMANAH_ML_URL || !env.AMANAH_ML_TOKEN) {
    throw new Error("AMANAH server-side configuration is missing.");
  }

  try {
    const response = await fetch(env.AMANAH_ML_URL, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${env.AMANAH_ML_TOKEN}`,
        "X-Scale-Up-Timeout": "600",
      },
      body: JSON.stringify({ inputs: input }),
    });

    if (!response.ok) {
      return unavailableResult(
        `ML endpoint unavailable (HTTP ${response.status}); human review required.`
      );
    }

    return (await response.json()) as AmanahResult;
  } catch (error) {
    return unavailableResult(
      `ML endpoint unavailable; human review required. ${String(error)}`
    );
  }
}
