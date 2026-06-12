import type { ClinicalEvent } from "../types/event";
import { EventCard } from "./EventCard";

interface Props {
  events: ClinicalEvent[];
}

export function TimelineView({ events }: Props) {
  if (events.length === 0) {
    return <div className="empty-box">No hay eventos clínicos registrados todavía.</div>;
  }

  return (
    <ol className="timeline-list">
      {events.map((event) => (
        <li key={event.id}>
          <EventCard event={event} />
        </li>
      ))}
    </ol>
  );
}
