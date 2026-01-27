"use client";

import Link from "next/link";
import type { ExperimentListItem } from "@/lib/types";

const mock: ExperimentListItem[] = [
  { id: 1, name: "Example (Week 1)", status: "queued", created_at: new Date().toISOString() },
];

export default function ExperimentTable() {
  return (
    <div className="rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-slate-600">
          <tr>
            <th className="px-4 py-3 text-left">ID</th>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Status</th>
            <th className="px-4 py-3 text-left">Created</th>
          </tr>
        </thead>
        <tbody>
          {mock.map((e) => (
            <tr key={e.id} className="border-t border-slate-200">
              <td className="px-4 py-3">
                <Link href={`/experiments/${e.id}`} className="text-slate-900 underline">
                  {e.id}
                </Link>
              </td>
              <td className="px-4 py-3">{e.name}</td>
              <td className="px-4 py-3">{e.status}</td>
              <td className="px-4 py-3">{new Date(e.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
