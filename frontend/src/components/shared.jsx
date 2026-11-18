import { useState, useEffect } from 'react'
import axios from 'axios'

export function useApi(url) {
  const [data, setData]     = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]   = useState(null)
  useEffect(() => {
    setLoading(true)
    axios.get(url)
      .then(r => { setData(r.data); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [url])
  return { data, loading, error }
}

export function Loading() {
  return (
    <div style={{ display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', height: 240, gap: 16 }}>
      <div className="spinner" />
      <span style={{ color:'var(--text-muted)', fontSize:'0.875rem' }}>Analysing Data…</span>
    </div>
  )
}

export function ErrorBanner({ msg }) {
  return (
    <div style={{ padding:'20px', borderRadius:12, background:'rgba(239,68,68,0.1)', border:'1px solid rgba(239,68,68,0.3)', color:'#FCA5A5', fontSize:'0.875rem' }}>
      ⚠️ {msg}
    </div>
  )
}

export function PageHeader({ title, subtitle, accent='pink' }) {
  const colors = { pink:'var(--pink)', blue:'var(--blue)', gold:'var(--gold)' }
  return (
    <div style={{ marginBottom: 28 }}>
      <div style={{ width: 48, height: 3, background: colors[accent], borderRadius: 2, marginBottom: 10 }} />
      <h1 style={{ fontFamily:'Rajdhani,sans-serif', fontWeight:700, fontSize:'2rem', lineHeight:1.1 }}>{title}</h1>
      {subtitle && <p style={{ color:'var(--text-muted)', marginTop:6, fontSize:'0.9rem' }}>{subtitle}</p>}
    </div>
  )
}

export function RankBadge({ rank }) {
  const cls = rank === 1 ? 'rank-1' : rank === 2 ? 'rank-2' : rank === 3 ? 'rank-3' : 'rank-other'
  return <span className={`rank-badge ${cls}`}>{rank}</span>
}

export function StatChip({ label, value, color='var(--text-secondary)' }) {
  return (
    <div style={{ display:'flex', flexDirection:'column', gap:2 }}>
      <span style={{ fontSize:'0.65rem', color:'var(--text-muted)', textTransform:'uppercase', letterSpacing:'0.08em' }}>{label}</span>
      <span style={{ fontWeight:700, color, fontSize:'0.95rem' }}>{value}</span>
    </div>
  )
}

export function Avatar({ name, size=44 }) {
  const initials = name ? name.split(' ').map(w=>w[0]).slice(0,2).join('').toUpperCase() : '?'
  const colors = ['#EA1A7F','#0EA5E9','#8B5CF6','#22C55E','#F97316','#EAB308']
  const color  = colors[(name||'').charCodeAt(0) % colors.length]
  return (
    <div style={{
      width: size, height: size, borderRadius:'50%',
      background: `linear-gradient(135deg, ${color}33, ${color}66)`,
      border: `2px solid ${color}55`,
      display:'flex', alignItems:'center', justifyContent:'center',
      fontWeight:700, fontSize: size * 0.33, color,
      flexShrink: 0,
    }}>
      {initials}
    </div>
  )
}

export function NationalityFlag({ country }) {
  const flags = {
    'India': '🇮🇳', 'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Australia': '🇦🇺',
    'Pakistan': '🇵🇰', 'West Indies': '🏏', 'South Africa': '🇿🇦',
    'New Zealand': '🇳🇿', 'Sri Lanka': '🇱🇰', 'Afghanistan': '🇦🇫',
    'Bangladesh': '🇧🇩', 'Zimbabwe': '🇿🇼', 'Ireland': '🇮🇪',
  }
  return <span title={country}>{flags[country] || '🌍'}</span>
}

export function fmt(n, decimals=2) {
  if (n === null || n === undefined || n === '' || isNaN(+n)) return '—'
  return (+n).toFixed(decimals)
}
