"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function Header() {
    const pathname = usePathname();
    const isHome = pathname === "/";

    return (
        <header className="bg-white border-b border-gray-200 px-8 py-4 flex items-center gap-4">
            {!isHome && (
                <Link href="/" className="text-gray-brand hover:text-brand text-sm">
                    ← Voltar
                </Link>
            )}
            <Link href="/" className="text-2xl font-bold text-brand tracking-tight">
                Dashboard Sensorweb
            </Link>
        </header>
    );
}