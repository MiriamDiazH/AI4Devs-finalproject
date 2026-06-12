"use client";

import { useState, useEffect } from "react";
import { patientApi } from "../../services/patientApi";
import { EncounterForm } from "../../components/EncounterForm";
import type { Patient } from "../../types/patient";

export default function EncountersPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [done, setDone] = useState("");

  useEffect(() => {
    patientApi.list().then(setPatients);
  }, []);

  return (
    <main className="page-wrap">
      <header className="page-header">
        <p className="eyebrow">Ingesta clínica</p>
        <h1>Registrar un nuevo encuentro</h1>
      </header>

      <section className="section-card">
        <div className="field" style={{ maxWidth: "380px" }}>
          <label htmlFor="enc-patient">Paciente</label>
          <select
            id="enc-patient"
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
            required
          >
            <option value="">-- selecciona --</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>

        {!selectedId ? (
          <p className="status-text">Selecciona un paciente para habilitar el formulario clínico.</p>
        ) : (
          <EncounterForm patientId={selectedId} onCreated={(id) => setDone(id)} />
        )}

        {done && <p className="status-text success">Encuentro creado correctamente: {done}</p>}
      </section>
    </main>
  );
}
