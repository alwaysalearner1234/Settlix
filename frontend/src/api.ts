export interface Incident { id: string; payment_id: string; type: string; status: string; priority: string; summary: string; created_at: string }
export interface Payment { id: string; supplier_id: string; amount: number; status: string; invoice_no: string }
const BASE = (import.meta as any).env?.VITE_API_URL ?? 'http://localhost:8000'
export async function fetchIncidents(): Promise<Incident[]> {
  try { const r = await fetch(`${BASE}/incidents`); return await r.json() }
  catch { return [{ id: 'inc-mock-1', payment_id: 'pay-mock-1', type: 'UNKNOWN_STATUS', status: 'OPEN', priority: 'P1', summary: 'Mock: ambiguous failure (API offline)', created_at: new Date().toISOString() }] }
}
