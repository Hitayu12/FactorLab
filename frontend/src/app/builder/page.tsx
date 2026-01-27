"use client";

import StrategyForm from "@/components/StrategyForm";
import RunButton from "@/components/RunButton";

export default function BuilderPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold">Strategy Builder</h1>
        <p className="text-sm text-slate-600">
          Define universe, factor(s), transforms, portfolio construction, and cost assumptions.
        </p>
      </header>

      <div className="rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <StrategyForm />
        <RunButton />
        <div className="text-xs text-slate-500">
          Week 1 scaffold: backend experiment endpoints land Week 7; factors/portfolio/backtest land Weeks 4–6.
        </div>
      </div>
    </div>
  );
}
