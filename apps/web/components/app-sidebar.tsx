"use client";

import { cn } from "@/lib/utils";
import {
  BadgeCheck,
  BookOpenText,
  Building2,
  FileBadge2,
  LayoutDashboard,
  WalletCards,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/admin", label: "Admin", icon: LayoutDashboard },
  { href: "/student", label: "Student", icon: BookOpenText },
  { href: "/institution", label: "Institution", icon: Building2 },
  { href: "/admin", label: "Verification", icon: BadgeCheck },
  { href: "/admin", label: "Payments", icon: WalletCards },
  { href: "/admin", label: "Documents", icon: FileBadge2 },
];

export function AppSidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-30 hidden h-screen w-72 border-r border-border/70 bg-card/80 px-4 py-6 backdrop-blur-xl md:block">
      <div className="mb-8 rounded-2xl bg-gradient-to-br from-indigo-600 to-violet-600 p-[1px] shadow-soft">
        <div className="rounded-2xl bg-card px-4 py-4">
          <p className="text-xl font-semibold text-foreground">ExamFlow</p>
          <p className="text-sm text-muted-foreground">by M.B. Technosoft</p>
        </div>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;

          return (
            <Link
              key={`${item.label}-${item.href}`}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-2xl px-3 py-2.5 text-sm font-medium transition",
                active
                  ? "bg-primary text-primary-foreground shadow-soft"
                  : "text-muted-foreground hover:bg-secondary hover:text-secondary-foreground",
              )}
            >
              <Icon size={17} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
