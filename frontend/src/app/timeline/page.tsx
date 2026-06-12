"use client";

import { useEffect, useState } from "react";
import { patientApi } from "../../services/patientApi";
import { timelineApi } from "../../services/timelineApi";
import { TimelineView } from "../../components/TimelineView";
import type { Patient } from "../../types/patient";
import type { ClinicalEvent } from "../../types/event";

export default function TimelinePage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [events, setEvents] = useState<ClinicalEvent[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    patientApi.list().then(setPatients);
  }, []);

  async function handleSelect(id: string) {
    setSelectedId(id);
    if (!id) { setEvents([]); return; }
    setLoading(true);
    const timeline = await timelineApi.getByPatientId(id);
    setEvents(timeline.events);
    setLoading(false);
  }

  return (
    <main className="page-wrap">
      <header className="page-header">
        <p className="eyebrow">Visor clínico</p>
        <h1>Timeline por paciente</h1>
      </header>

      <section className="section-card">
        <div className="field" style={{ maxWidth: "380px" }}>
          <label htmlFor="timeline-patient">Paciente</label>
          <select
            id="timeline-patient"
            value={selectedId}
            onChange={(e) => handleSelect(e.target.value)}
          >
            <option value="">-- selecciona --</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>

        {loading ? <p className="status-text">Cargando timeline...</p> : <TimelineView events={events} />}
      </section>
    </main>
  );
}
