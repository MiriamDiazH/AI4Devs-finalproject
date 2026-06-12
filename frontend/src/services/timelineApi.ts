import type { ClinicalEvent } from "../types/event";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const timelineApi = {
  getByPatientId: async (patientId: string): Promise<{ patient_id: string; events: ClinicalEvent[] }> => {
    const res = await fetch(`${BASE}/patients/${patientId}/timeline`);
    if (!res.ok) throw new Error("Failed to fetch timeline");
    return res.json();
  },
};
