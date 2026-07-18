"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchDevices } from "@/lib/api";

export default function Home() {
  const { data: devices, isLoading, error } = useQuery({
    queryKey: ["devices"],
    queryFn: fetchDevices,
    refetchInterval: 5000,
  });

  if (isLoading) return <p>Carregando...</p>;
  if (error) return <p>Erro ao carregar dispositivos</p>;


  return (
    <main style={{ padding: "2rem" }}>
      <h1>Dashboard SensorWeb</h1>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
        {devices?.map((device) => (
          <div key={device.id} style={{ border: "1px solid #ccc", padding: "1rem", borderRadius: "8px" }}>
            <h2>{device.name}</h2>
            <ul>
              {device.current_state.map((metric) => (
                <li key={metric.metric_key}>
                  {metric.metric_type}: {metric.value}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </main>  
  );
}
