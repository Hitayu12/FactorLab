"use client";

import type { SeriesPoint } from "@/lib/types";

export default function Turnover({ series }: { series: SeriesPoint[] }) {
  return (
    <div className="rounded-2xl border border-slate-200 p-5 shadow-sm">
      <div className="text-sm font-medium">Turnover</div>
      <div className="mt-3 h-56 rounded-xl bg-slate-50 flex items-center justify-center text-xs text-slate-500">
        Chart placeholder
      </div>
    </div>
  );
}
