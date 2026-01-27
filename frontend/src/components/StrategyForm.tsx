"use client";

import { useState } from "react";

const CORE_CROSS_ASSET = ["SPY","QQQ","IWM","EFA","EEM","TLT","IEF","SHY","LQD","HYG","GLD","DBC","VNQ"];

export default function StrategyForm() {
  const [preset, setPreset] = useState("Core Cross-Asset");
  const [start, setStart] = useState("2006-01-01");
  const [end, setEnd] = useState("2025-12-31");

  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-3">
        <div>
          <label className="text-xs text-slate-600">Universe Preset</label>
          <select
            value={preset}
            onChange={(e) => setPreset(e.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm"
          >
            <option>Core Cross-Asset</option>
          </select>
          <div className="mt-2 text-xs text-slate-500">Tickers: {CORE_CROSS_ASSET.join(", ")}</div>
        </div>

        <div>
          <label className="text-xs text-slate-600">Start</label>
          <input
            value={start}
            onChange={(e) => setStart(e.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm"
            placeholder="YYYY-MM-DD"
          />
        </div>

        <div>
          <label className="text-xs text-slate-600">End</label>
          <input
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm"
            placeholder="YYYY-MM-DD"
          />
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 p-4">
        <div className="text-sm font-medium">Factor & Portfolio Controls</div>
        <div className="mt-2 text-xs text-slate-500">
          Week 1 scaffold: dynamic factor registry and portfolio controls land Weeks 4–6.
        </div>
      </div>
    </div>
  );
}
