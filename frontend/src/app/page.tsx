"use client";

import { DeviceCard } from "@/components/DeviceCard";
import { useQuery } from "@tanstack/react-query";
import { fetchDevices } from "@/lib/api";
import Link from "next/link";

export default function Home() {
  const { data: devices, isLoading, error } = useQuery({
    queryKey: ["devices"],
    queryFn: fetchDevices,
    refetchInterval: 5000,
  });

  if (isLoading) return <p>Carregando...</p>;
  if (error) return <p>Erro ao carregar dispositivos</p>;


  return (
      <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
        {devices?.map((device) => (
          <Link key={device.id} href={`/devices/${device.id}`}>
            <DeviceCard device={device} />
          </Link>
        ))}
      </div>
  );
}
