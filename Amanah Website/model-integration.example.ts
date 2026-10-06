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

export async function analyzeWithAmanah(
  input: AmanahInput,
  env: { AMANAH_ML_URL: string; AMANAH_ML_TOKEN: string }
): Promise<AmanahResult> {
  if (!env.AMANAH_ML_URL || !env.AMANAH_ML_TOKEN) {
    throw new Error("AMANAH server-side configuration is missing.");
  }

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
    throw new Error(`AMANAH endpoint failed with HTTP ${response.status}`);
  }

  return (await response.json()) as AmanahResult;
}
