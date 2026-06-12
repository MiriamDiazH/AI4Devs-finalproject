import Link from "next/link";
import type { Patient } from "../types/patient";

interface Props {
  patient: Patient;
}

export function PatientCard({ patient }: Props) {
  return (
    <article className="patient-card">
      <p className="eyebrow">Paciente</p>
      <h2>{patient.name}</h2>
      <p>
        Nacimiento: {patient.birth_date} · Sexo: {patient.sex}
      </p>
      <Link className="link-inline" href={`/patients/${patient.id}`}>
        Ver perfil clínico
      </Link>
    </article>
  );
}
