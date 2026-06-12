import type { ClinicalEvent } from "../types/event";

const CATEGORY_LABELS: Record<string, string> = {
  diagnosis: "Diagnóstico",
  medication: "Medicación",
  lab: "Laboratorio",
  procedure: "Procedimiento",
  symptom: "Síntoma",
  allergy: "Alergia",
  other: "Otro",
};

interface Props {
  event: ClinicalEvent;
}

export function EventCard({ event }: Props) {
  return (
    <article className="event-card">
      <div className="event-meta">
        <span className="event-chip">{CATEGORY_LABELS[event.category] ?? event.category}</span>
        <span>Confianza: {(event.confidence * 100).toFixed(0)}%</span>
        {event.event_date && <span>Fecha: {event.event_date}</span>}
      </div>
      <h3>{event.title}</h3>
      <p>{event.description}</p>
      <details>
        <summary>Fuente clínica</summary>
        <blockquote>{event.source_quote}</blockquote>
      </details>
    </article>
  );
}
