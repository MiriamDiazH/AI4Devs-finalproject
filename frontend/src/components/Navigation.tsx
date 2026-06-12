"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/", label: "Inicio" },
  { href: "/patients", label: "Pacientes" },
  { href: "/encounters", label: "Encuentros" },
  { href: "/timeline", label: "Timeline" },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <header className="topbar">
      <div className="topbar-inner">
        <Link href="/" className="brand">
          <span className="brand-mark" aria-hidden />
          AuditCare Timeline
        </Link>
        <nav className="nav-links">
          {NAV_ITEMS.map((item) => {
            const isActive = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`nav-pill${isActive ? " active" : ""}`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
