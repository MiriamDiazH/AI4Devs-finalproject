import Link from "next/link";

export default function Home() {
  return (
    <main className="page-wrap">
      <section className="hero-panel">
        <p className="eyebrow">AI4Devs Final Project · Entrega 2</p>
        <h1>Timeline clínico útil en minutos, no en horas</h1>
        <p className="lead">
          AuditCare transforma notas clínicas en una secuencia temporal
          navegable, con trazabilidad y contexto longitudinal por paciente usando
          Statewave como memoria duradera.
        </p>
        <div className="hero-actions">
          <Link href="/patients" className="button primary">
            Ver pacientes
          </Link>
          <Link href="/timeline" className="button secondary">
            Abrir timeline
          </Link>
        </div>
      </section>

      <section className="section-card">
        <div className="page-header">
          <p className="eyebrow">Flujo de trabajo</p>
          <h2>Del texto libre al contexto clínico accionable</h2>
        </div>
        <div className="card-grid">
          <article className="feature-card">
            <span className="feature-tag">1. Registro</span>
            <h3>Pacientes sintéticos</h3>
            <p>Alta rápida de pacientes de prueba con datos demográficos mínimos.</p>
          </article>
          <article className="feature-card">
            <span className="feature-tag">2. Ingesta</span>
            <h3>Encuentros clínicos</h3>
            <p>Notas médicas en texto libre por consulta, revisión o urgencias.</p>
          </article>
          <article className="feature-card">
            <span className="feature-tag">3. Extracción</span>
            <h3>IA con memoria</h3>
            <p>Statewave conserva contexto longitudinal y alimenta la extracción de eventos.</p>
          </article>
        </div>
      </section>
    </main>
  );
}
