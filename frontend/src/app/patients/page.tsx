"use client";

import { useEffect, useState } from "react";
import { patientApi } from "../../services/patientApi";
import { PatientCard } from "../../components/PatientCard";
import type { Patient } from "../../types/patient";

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [sex, setSex] = useState("M");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    patientApi.list().then(setPatients).finally(() => setLoading(false));
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    setError("");
    try {
      const patient = await patientApi.create({ name, birth_date: birthDate, sex });
      setPatients((prev) => [...prev, patient]);
      setName("");
      setBirthDate("");
      setSex("M");
    } catch {
      setError("No se pudo crear el paciente. Revisa que el backend este activo.");
    } finally {
      setCreating(false);
    }
  }

  return (
    <main className="page-wrap">
      <header className="page-header">
        <p className="eyebrow">Gestor de pacientes</p>
        <h1>Pacientes de ejemplo y seguimiento</h1>
        <p className="lead">
          Crea nuevos pacientes sintéticos y accede al perfil individual para añadir
          encuentros o lanzar extracción clínica con IA.
        </p>
      </header>

      <section className="section-card">
        <h2>Alta rápida</h2>
        <form className="create-form" onSubmit={handleCreate}>
          <div className="field">
            <label htmlFor="patient-name">Nombre</label>
            <input
              id="patient-name"
              placeholder="Ej. Marta Lozano"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="field">
            <label htmlFor="patient-birth">Nacimiento</label>
            <input
              id="patient-birth"
              type="date"
              value={birthDate}
              onChange={(e) => setBirthDate(e.target.value)}
              required
            />
          </div>

          <div className="field">
            <label htmlFor="patient-sex">Sexo</label>
            <select id="patient-sex" value={sex} onChange={(e) => setSex(e.target.value)}>
              <option value="M">M</option>
              <option value="F">F</option>
              <option value="O">Otro</option>
            </select>
          </div>

          <button className="button primary" type="submit" disabled={creating}>
            {creating ? "Creando..." : "Crear paciente"}
          </button>
        </form>
        {error && <p className="status-text error">{error}</p>}
      </section>

      <section className="section-card">
        <h2>Listado</h2>
        {loading ? (
          <p className="status-text">Cargando pacientes...</p>
        ) : patients.length === 0 ? (
          <div className="empty-box">No hay pacientes todavía. Crea el primero desde el formulario.</div>
        ) : (
          <div className="card-grid">
            {patients.map((p) => (
              <PatientCard key={p.id} patient={p} />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
