import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="text-sm text-slate-500">FactorLab</div>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">
          Cross-Asset Factor Research and Backtesting Engine
        </h1>
        <p className="mt-3 text-slate-700">
          A reproducible research terminal for cross-asset ETF signals, portfolio construction,
          and backtesting with explicit controls against common failure modes.
        </p>
        <div className="mt-6 flex gap-3">
          <Link className="rounded-xl bg-slate-900 px-4 py-2 text-white" href="/builder">
            Open Strategy Builder
          </Link>
          <Link className="rounded-xl border border-slate-300 px-4 py-2" href="/experiments">
            Experiment Library
          </Link>
        </div>
      </div>
    </div>
  );
}
