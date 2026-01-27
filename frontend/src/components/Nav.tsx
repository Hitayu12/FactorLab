import Link from "next/link";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/builder", label: "Strategy Builder" },
  { href: "/experiments", label: "Experiment Library" },
  { href: "/compare", label: "Compare" },
];

export default function Nav() {
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-baseline gap-3">
          <div className="text-lg font-semibold">FactorLab</div>
          <div className="hidden text-sm text-slate-500 md:block">
            Cross-Asset Factor Research and Backtesting Engine
          </div>
        </div>
        <div className="flex gap-4 text-sm">
          {navItems.map((it) => (
            <Link key={it.href} href={it.href} className="text-slate-700 hover:text-slate-900">
              {it.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
