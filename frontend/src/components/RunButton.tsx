"use client";

import { useState } from "react";

export default function RunButton() {
  const [status, setStatus] = useState<"idle" | "queued">("idle");
  const [experimentId, setExperimentId] = useState<string | null>(null);

  const onRun = async () => {
    // Week 1 scaffold: backend POST /experiments lands Week 7.
    setStatus("queued");
    setExperimentId("pending");
  };

  return (
    <div className="flex items-center gap-3">
      <button onClick={onRun} className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white">
        Run
      </button>
      <div className="text-sm text-slate-700">
        Status: <span className="font-medium">{status}</span>
      </div>
      {experimentId && <div className="text-xs text-slate-500">experiment_id: {experimentId}</div>}
    </div>
  );
}
