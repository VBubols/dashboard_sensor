import { Device, Reading } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchDevices(): Promise<Device[]> {
    const res = await fetch(`${API_URL}/devices/`);
    if (!res.ok) {
        throw new Error("Falha ao buscar devices");
    }
    return res.json();
}

export async function fetchDeviceReadings(deviceId: number): Promise<Reading[]> {
    const res = await fetch(`${API_URL}/devices/${deviceId}/readings`);
    if (!res.ok) {
        throw new Error("Falha ao buscar readings");
    }
    return res.json();
}