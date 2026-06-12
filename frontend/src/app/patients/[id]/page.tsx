"use client";

import { useEffect, useState } from "react";
import { use } from "react";
import { patientApi } from "../../../services/patientApi";
import { encounterApi } from "../../../services/encounterApi";
import { timelineApi } from "../../../services/timelineApi";
import { EncounterForm } from "../../../components/EncounterForm";
import { TimelineView } from "../../../components/TimelineView";
import StatewaveStatus from "../../../components/StatewaveStatus";
import type { Encounter } from "../../../types/encounter";
import type { Patient } from "../../../types/patient";
import type { ClinicalEvent } from "../../../types/event";

export default function PatientDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [patient, setPatient] = useState<Patient | null>(null);
  const [events, setEvents] = useState<ClinicalEvent[]>([]);
  const [encounters, setEncounters] = useState<Encounter[]>([]);
  const [extracting, setExtracting] = useState(false);
  const [extractInfo, setExtractInfo] = useState<string>("");

  useEffect(() => {
    patientApi.get(id).then(setPatient);
    timelineApi.getByPatientId(id).then((r) => setEvents(r.events));
    encounterApi.listByPatient(id).then(setEncounters);
  }, [id]);

  async function handleEncounterCreated(encounterId: string) {
    setExtracting(true);
    setExtractInfo("");
    try {
      const extracted = await encounterApi.extractEvents(encounterId);
      if (Array.isArray(extracted) && extracted.length === 0) {
        setExtractInfo("Encuentro guardado. No se extrajeron eventos todavía.");
      }
    } catch {
      setExtractInfo("Encuentro guardado. La extracción falló temporalmente.");
    } finally {
      const [timeline, patientEncounters] = await Promise.all([
        timelineApi.getByPatientId(id),
        encounterApi.listByPatient(id),
      ]);
      setEvents(timeline.events);
      setEncounters(patientEncounters);
      setExtracting(false);
    }
  }

  if (!patient) {
    return (
      <main className="page-wrap">
        <div className="section-card">
          <p className="status-text">Cargando perfil de paciente...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="page-wrap">
      <header className="page-header">
        <p className="eyebrow">Paciente</p>
        <h1>{patient.name}</h1>
        <p className="lead">Nacimiento: {patient.birth_date} · Sexo: {patient.sex}</p>
      </header>

      <div className="split-layout">
        <section className="section-card">
          <h2>Nuevo encuentro clínico</h2>
          <p className="status-text">
            Añade una nota en texto libre. Al guardarla, se dispara extracción con IA
            y se actualiza la línea temporal.
          </p>
          <EncounterForm patientId={id} onCreated={handleEncounterCreated} />
          {extracting && <p className="status-text">Extrayendo eventos con IA y memoria Statewave...</p>}
          {extractInfo && <p className="status-text">{extractInfo}</p>}

          <div style={{ marginTop: "1rem" }}>
            <h3>Encuentros guardados ({encounters.length})</h3>
            {encounters.length === 0 ? (
              <p className="status-text">Todavia no hay encuentros guardados.</p>
            ) : (
              <ul className="timeline-list" style={{ marginTop: "0.75rem" }}>
                {encounters.map((enc) => (
                  <li key={enc.id} className="timeline-item">
                    <p className="status-text" style={{ marginBottom: "0.25rem" }}>
                      {enc.date} · {enc.type}
                    </p>
                    <p>{enc.note_text}</p>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>

        <section className="section-card">
          <h2>Timeline clínico</h2>
          <StatewaveStatus patientId={id} />
          <div style={{ marginTop: "1rem" }} />
          <TimelineView events={events} />
        </section>
      </div>
    </main>
  );
}
