"use client";

import type { Metrics } from "@/lib/types";

export default function MetricCards({ metrics }: { metrics: Partial<Metrics> }) {
  const items = [
    ["CAGR", metrics.cagr],
    ["Vol", metrics.vol],
    ["Sharpe", metrics.sharpe],
    ["Sortino", metrics.sortino],
    ["Max DD", metrics.max_drawdown],
    ["Turnover", metrics.turnover_mean],
  ] as const;

  return (
    <div className="grid gap-3 md:grid-cols-6">
      {items.map(([label, value]) => (
        <div key={label} className="rounded-2xl border border-slate-200 p-4 shadow-sm">
          <div className="text-xs text-slate-500">{label}</div>
          <div className="mt-1 text-sm font-semibold">{value ?? "—"}</div>
        </div>
      ))}
    </div>
  );
}
