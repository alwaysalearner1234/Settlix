import { PaymentTimeline } from '../components/PaymentTimeline'
import { EvidencePanel } from '../components/EvidencePanel'
import { DecisionPanel } from '../components/DecisionPanel'
export function IncidentDetail() {
  return (
    <div className="space-y-4">
      <h2 className="font-bold">Incident detail</h2>
      <PaymentTimeline />
      <EvidencePanel />
      <DecisionPanel />
    </div>
  )
}
