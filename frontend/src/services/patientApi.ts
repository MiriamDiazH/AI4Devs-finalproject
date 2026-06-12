import type { Patient } from "../types/patient";

export interface StatewaveStatus {
  subject_id: string;
  is_available: boolean;
  status: "healthy" | "no_data" | "error";
  message: string;
  context_preview: string | null;
}

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const patientApi = {
  list: async (): Promise<Patient[]> => {
    const res = await fetch(`${BASE}/patients`);
    if (!res.ok) throw new Error("Failed to list patients");
    return res.json();
  },

  get: async (id: string): Promise<Patient> => {
    const res = await fetch(`${BASE}/patients/${id}`);
    if (!res.ok) throw new Error("Patient not found");
    return res.json();
  },

  create: async (data: Omit<Patient, "id">): Promise<Patient> => {
    const res = await fetch(`${BASE}/patients`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create patient");
    return res.json();
  },

  getStatewaveStatus: async (id: string): Promise<StatewaveStatus> => {
    const res = await fetch(`${BASE}/patients/${id}/statewave-status`);
    if (!res.ok) throw new Error("Failed to fetch Statewave status");
    return res.json();
  },
};
