"use client";

import ExperimentTable from "@/components/ExperimentTable";

export default function ExperimentsPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold">Experiment Library</h1>
        <p className="text-sm text-slate-600">
          Browse experiments and key metrics once results exist.
        </p>
      </header>
      <ExperimentTable />
    </div>
  );
}
