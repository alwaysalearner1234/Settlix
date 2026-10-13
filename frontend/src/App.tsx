import { Overview } from './pages/Overview'
import { IncidentDetail } from './pages/IncidentDetail'
export default function App() {
  const hash = window.location.hash
  return (
    <div className="mx-auto max-w-4xl p-6">
      <header className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-black">Settlix <span className="text-sm font-normal text-gray-500">Phase 1</span></h1>
        <nav className="text-sm"><a href="#/" className="underline">Overview</a></nav>
      </header>
      {hash.startsWith('#/incident/') ? <IncidentDetail /> : <Overview />}
    </div>
  )
}
