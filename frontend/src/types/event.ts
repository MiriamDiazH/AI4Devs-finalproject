export type ClinicalEvent = {
  id: string;
  encounter_id: string;
  patient_id: string;
  category: string;
  title: string;
  description: string;
  confidence: number;
  source_quote: string;
  event_date: string | null;
};
