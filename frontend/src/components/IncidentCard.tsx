export type { Incident } from '../api'
import type { Incident } from '../api'
export function IncidentCard({ inc }: { inc: Incident }) {
  return (
    <a href={`#/incident/${inc.id}`} className="block rounded-xl border p-4 shadow-sm hover:shadow">
      <div className="flex justify-between text-sm">
        <span className="font-semibold">{inc.type}</span>
        <span className="rounded bg-red-100 px-2 py-0.5 text-red-700">{inc.priority}</span>
      </div>
      <p className="mt-2 text-sm text-gray-700">{inc.summary}</p>
      <p className="mt-1 text-xs text-gray-400">{inc.id.slice(0, 8)} · payment {inc.payment_id.slice(0, 8)} · {inc.status}</p>
    </a>
  )
}
