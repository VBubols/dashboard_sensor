"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { fetchDeviceReadings } from "@/lib/api";

export default function DeviceHistory() {
    const params = useParams();
    const deviceId = Number(params.id);

    const { data: readings, isLoading, error } = useQuery({
        queryKey: ["readings", deviceId],
        queryFn: () => fetchDeviceReadings(deviceId),
        refetchInterval: 5000,
    });

    if (isLoading) return <p>Carregando...</p>;
    if (error) return <p>Erro ao carregar dispositivos</p>;

    const metricKeys = Array.from(new Set(readings?.map((r) => r.metric_key)));

    const chartData = readings
        ?.slice()
        .reverse()
        .reduce((acc: any[], reading) => {
            const existing = acc.find((item) => item.timestamp === reading.timestamp);
            if (existing) {
                existing[reading.metric_key] = reading.value;
            } else {
                acc.push({ timestamp: reading.timestamp, [reading.metric_key]: reading.value });
            }
            return acc;
        }, []);

        const colors = ["#8884d8", "#82ca9d", "#ffc658", "#ff7f7f", "#8dd1e1", "#a4de6c"];

    return (
        <main style={{ padding: "2rem" }}>
            <h1>Histórico do Dispositivo {deviceId}</h1>
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" tick={false} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {metricKeys.map((key, i) => (
                        <Line key={key}  type="monotone" dataKey={key} stroke={colors[i % colors.length]} dot={false} />
                    ))}
                </LineChart>
            </ResponsiveContainer>
        </main>
    );
}   