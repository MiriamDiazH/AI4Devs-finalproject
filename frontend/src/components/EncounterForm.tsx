"use client";

import { useState } from "react";
import { encounterApi } from "../services/encounterApi";

interface Props {
  patientId: string;
  onCreated?: (encounterId: string) => void;
}

export function EncounterForm({ patientId, onCreated }: Props) {
  const [date, setDate] = useState("");
  const [type, setType] = useState("consulta");
  const [noteText, setNoteText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const encounter = await encounterApi.create({
        patient_id: patientId,
        date,
        type,
        note_text: noteText,
      });
      onCreated?.(encounter.id);
      setDate("");
      setType("consulta");
      setNoteText("");
    } catch {
      setError("Error al crear el encuentro.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="encounter-form">
      <div className="field">
        <label htmlFor="enc-date">Fecha</label>
        <input id="enc-date" type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
      </div>

      <div className="field">
        <label htmlFor="enc-type">Tipo</label>
        <input id="enc-type" value={type} onChange={(e) => setType(e.target.value)} required />
      </div>

      <div className="field">
        <label htmlFor="enc-note">Nota clínica</label>
        <textarea
          id="enc-note"
          rows={6}
          value={noteText}
          onChange={(e) => setNoteText(e.target.value)}
          required
        />
      </div>

      {error && <p className="status-text error">{error}</p>}
      <button className="button primary" type="submit" disabled={loading}>
        {loading ? "Guardando..." : "Crear encuentro"}
      </button>
    </form>
  );
}
