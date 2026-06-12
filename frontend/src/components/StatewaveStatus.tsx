"use client";

import { useEffect, useState } from "react";
import { patientApi, type StatewaveStatus } from "../services/patientApi";

export default function StatewaveStatus({ patientId }: { patientId: string }) {
  const [status, setStatus] = useState<StatewaveStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        setLoading(true);
        const data = await patientApi.getStatewaveStatus(patientId);
        setStatus(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error fetching Statewave status");
      } finally {
        setLoading(false);
      }
    };

    fetch();
  }, [patientId]);

  if (loading) return <p className="text-gray-500 text-sm">Loading Statewave status...</p>;

  if (!status) return null;

  const statusColors = {
    healthy: "bg-green-50 border-green-200 text-green-800",
    no_data: "bg-yellow-50 border-yellow-200 text-yellow-800",
    error: "bg-red-50 border-red-200 text-red-800",
  };

  const statusEmoji = {
    healthy: "✓",
    no_data: "◐",
    error: "✕",
  };

  return (
    <div className={`p-4 rounded-lg border ${statusColors[status.status]}`}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-lg">{statusEmoji[status.status]}</span>
        <h3 className="font-semibold">Statewave Integration</h3>
      </div>
      <p className="text-sm mb-2">{status.message}</p>
      <p className="text-xs opacity-75">Subject: <code>{status.subject_id}</code></p>
      {status.context_preview && (
        <details className="text-xs mt-2 opacity-75">
          <summary className="cursor-pointer font-semibold">Memory preview</summary>
          <pre className="mt-1 p-2 bg-black bg-opacity-5 rounded overflow-x-auto max-h-32 overflow-y-auto">
            {status.context_preview}
          </pre>
        </details>
      )}
    </div>
  );
}
