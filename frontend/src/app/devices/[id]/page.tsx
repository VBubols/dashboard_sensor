"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { fetchDevices, fetchDeviceReadings } from "@/lib/api";
import { Reading } from "@/lib/types";

const METRIC_COLORS: Record<string, string> = {
    TempC_SHT: "#01a19e",
    Ext_TempC_SHT: "#ff8f33",
    Hum_SHT: "#01a19e",
    Ext_Hum_SHT: "#ff8f33",
    Bateria: "#636364",
};

function toChartData(readings: Reading[]) {
  const byTimestamp: Record<string, any> = {};
  for (const r of readings) {
    if (!byTimestamp[r.timestamp]) {
        byTimestamp[r.timestamp] = { timestamp: r.timestamp };
    }
    byTimestamp[r.timestamp][r.metric_key] = r.value;
  }
  return Object.values(byTimestamp).sort((a, b) =>
    a.timestamp.localeCompare(b.timestamp)
  );
}

type MetricChartProps = {
  metricKey: string;
  readings: Reading[];
};

function MetricChart({ metricKey, readings }: MetricChartProps) {
  const chartData = toChartData(readings);
  const label = readings[0]?.label ?? metricKey;
  const unit = readings[0]?.unit ?? "";
  const cor = METRIC_COLORS[metricKey] ?? "#01a19e";

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
      <h3 className="text-lg font-bold text-brand-dark mb-4">{label}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
          <XAxis dataKey="timestamp" tick={false} />
          <YAxis unit={unit} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey={metricKey}
            stroke={cor}
            dot={false}
            strokeWidth={2}
            name={label}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function DeviceHistory() {
  const params = useParams();
  const deviceId = Number(params.id);

  const { data: readings, isLoading, error } = useQuery({
    queryKey: ["readings", deviceId],
    queryFn: () => fetchDeviceReadings(deviceId),
    refetchInterval: 5000,
  });

  const { data: devices } = useQuery({
  queryKey: ["devices"],
  queryFn: fetchDevices,
  });

  const device = devices?.find((d) => d.id === deviceId);
  const deviceName = device?.name ?? `Dispositivo ${deviceId}`;

  if (isLoading) return <p>Carregando...</p>;
  if (error) return <p>Erro ao carregar histórico.</p>;

  const todosReadings = readings ?? [];
  const metricasExibidas = ["TempC_SHT", "Ext_TempC_SHT", "Hum_SHT", "Ext_Hum_SHT"];

  return (
    <div>
      <h1 className="text-2xl font-bold text-brand-dark mb-6">
        Histórico — {deviceName}
      </h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {metricasExibidas.map((metricKey) => {
          const readingsDaMetrica = todosReadings.filter(
            (r) => r.metric_key === metricKey
          );
          if (readingsDaMetrica.length === 0) return null;
          return (
            <MetricChart
              key={metricKey}
              metricKey={metricKey}
              readings={readingsDaMetrica}
            />
          );
        })}
      </div>
    </div>
  );
}