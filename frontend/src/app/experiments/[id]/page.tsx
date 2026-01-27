"use client";

import { useParams } from "next/navigation";
import MetricCards from "@/components/MetricCards";
import EquityCurve from "@/components/EquityCurve";
import Drawdown from "@/components/Drawdown";
import RollingSharpe from "@/components/RollingSharpe";
import Turnover from "@/components/Turnover";
import StatusPill from "@/components/StatusPill";

export default function ExperimentDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Results Explorer</h1>
          <div className="text-sm text-slate-600">Experiment ID: {id}</div>
        </div>
        <StatusPill status="queued" />
      </header>

      <MetricCards metrics={{}} />
      <div className="grid gap-4 md:grid-cols-2">
        <EquityCurve series={[]} />
        <Drawdown series={[]} />
        <RollingSharpe series={[]} />
        <Turnover series={[]} />
      </div>
    </div>
  );
}
