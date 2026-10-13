export function KpiCards({ total }: { total: number }) {
  const cards = [['Open incidents', total], ['Duplicates prevented', 1], ['Loss avoided', '$12,500']]
  return (
    <div className="grid grid-cols-3 gap-3">
      {cards.map(([k, v]) => (
        <div key={k as string} className="rounded-xl border p-4">
          <div className="text-xs text-gray-500">{k}</div>
          <div className="text-2xl font-bold">{v}</div>
        </div>
      ))}
    </div>
  )
}
