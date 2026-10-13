export function PaymentTimeline() {
  const steps = ['CREATED', 'SENT', 'BANK_ACK_PENDING', 'AGENT_INVESTIGATING', 'ESCALATED']
  return (
    <ol className="border-l pl-4 text-sm">
      {steps.map(s => <li key={s} className="py-1">● {s}</li>)}
    </ol>
  )
}
