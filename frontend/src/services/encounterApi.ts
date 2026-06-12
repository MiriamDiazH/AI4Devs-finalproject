import type { Encounter } from "../types/encounter";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const encounterApi = {
  create: async (data: Omit<Encounter, "id">): Promise<Encounter> => {
    const res = await fetch(`${BASE}/encounters`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create encounter");
    return res.json();
  },

  listByPatient: async (patientId: string): Promise<Encounter[]> => {
    const res = await fetch(`${BASE}/encounters/patient/${patientId}`);
    if (!res.ok) throw new Error("Failed to list encounters");
    return res.json();
  },

  extractEvents: async (encounterId: string) => {
    const res = await fetch(`${BASE}/encounters/${encounterId}/extract-events`, {
      method: "POST",
    });
    if (!res.ok) throw new Error("Failed to extract events");
    return res.json();
  },
};
