import { useEffect, useState } from 'react'
import { fetchIncidents, type Incident } from '../api'
import { IncidentCard } from '../components/IncidentCard'
import { KpiCards } from '../components/KpiCards'
export function Overview() {
  const [incs, setIncs] = useState<Incident[]>([])
  useEffect(() => { fetchIncidents().then(setIncs) }, [])
  return (
    <div className="space-y-4">
      <KpiCards total={incs.length} />
      <h2 className="font-bold">Incidents</h2>
      <div className="grid gap-3">{incs.map(i => <IncidentCard key={i.id} inc={i} />)}</div>
    </div>
  )
}
