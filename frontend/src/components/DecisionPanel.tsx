export function DecisionPanel() {
  return (
    <div className="rounded-xl border border-amber-300 bg-amber-50 p-4 text-sm">
      <div className="font-bold">Decision: ESCALATE (54% confidence)</div>
      <p>Original status ambiguous — duplicate blocked, human review requested.</p>
    </div>
  )
}
