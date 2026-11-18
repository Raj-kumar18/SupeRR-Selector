import { useState } from 'react'
import { useApi, Loading, ErrorBanner, PageHeader, RankBadge, Avatar, NationalityFlag, StatChip, fmt } from '../components/shared'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function BowlerRow({ player, rank, expanded, onToggle }) {
  const econSupp = +player.econ_suppression
  return (
    <>
      <tr onClick={onToggle} style={{ cursor:'pointer', transition:'background 0.2s' }}>
        <td><RankBadge rank={rank} /></td>
        <td>
          <div style={{ display:'flex', alignItems:'center', gap:10 }}>
            <Avatar name={player.player_name} size={36} />
            <div>
              <div style={{ fontWeight:700, fontSize:'0.92rem', color:'#FFFFFF' }}>{player.player_name}</div>
              <div style={{ fontSize:'0.72rem', color:'var(--text-muted)' }}>
                <NationalityFlag country={player.team_name} /> {player.team_name}
              </div>
            </div>
          </div>
        </td>
        <td><span style={{ color:'var(--gold)', fontWeight:800, fontSize:'0.95rem' }}>{fmt(player.reliability_score,1)}%</span></td>
        <td style={{ color:'var(--green)', fontWeight:700 }}>{fmt(player.press_economy,2)}</td>
        <td style={{ color:'var(--blue)' }}>{fmt(player.norm_economy,2)}</td>
        <td>
          <span style={{ color: econSupp >= 0 ? 'var(--pink)' : '#EF4444', fontWeight:700 }}>
            {econSupp >= 0 ? '+' : ''}{fmt(econSupp,2)} RPO
          </span>
        </td>
        <td style={{ fontWeight:700, color:'#F43FA0' }}>{player.press_wickets}</td>
        <td>{player.press_matches}</td>
        <td style={{ color:'var(--blue)', fontWeight:600 }}>{fmt(player.press_dot_pct,1)}%</td>
        <td><span style={{ color:'var(--green)', fontWeight:600 }}>+{fmt(player.dot_lift,1)}%</span></td>
      </tr>
      {expanded && (
        <tr>
          <td colSpan={10} style={{ background:'rgba(14,165,233,0.06)', borderTop:'1px solid rgba(14,165,233,0.2)', borderBottom:'1px solid rgba(14,165,233,0.2)' }}>
            <div style={{ padding:'16px 20px' }}>
              <div style={{ fontSize:'0.75rem', fontWeight:700, color:'var(--blue)', textTransform:'uppercase', letterSpacing:'0.08em', marginBottom:12 }}>
                Detailed Bowling Breakdown — {player.player_name}
              </div>
              <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(130px, 1fr))', gap:14 }}>
                <StatChip label="Normal Wickets" value={player.norm_wickets} />
                <StatChip label="Press Wickets" value={player.press_wickets} color="var(--pink)" />
                <StatChip label="Press Legal Balls" value={player.press_legal_balls} />
                <StatChip label="Press Overs" value={fmt(player.press_overs,1)} />
                <StatChip label="Normal Bowling SR" value={fmt(player.norm_strike_rate,1)} />
                <StatChip label="Press Bowling SR" value={fmt(player.press_strike_rate,1)} color="var(--gold)" />
                <StatChip label="Normal Average" value={fmt(player.norm_average,1)} />
                <StatChip label="Press Average" value={fmt(player.press_average,1)} color="var(--blue)" />
                <StatChip label="Norm Dot %" value={fmt(player.norm_dot_pct,1)+'%'} />
                <StatChip label="Press Dot %" value={fmt(player.press_dot_pct,1)+'%'} color="var(--green)" />
                <StatChip label="Dot Lift" value={'+'+fmt(player.dot_lift,1)+'%'} color="var(--green)" />
                <StatChip label="Boundary Prevention" value={fmt(player.boundary_prevention,1)+'%'} color="var(--gold)" />
                <StatChip label="Confidence Factor" value={fmt(player.confidence_factor,2)} color="var(--gold)" />
              </div>
            </div>
          </td>
        </tr>
      )}
    </>
  )
}

export default function BowlersIntelligence() {
  const { data: topData, loading: topLoading, error: topError } = useApi('/api/overall/bowlers')
  const { data: eligibleData, loading: eligLoading } = useApi('/api/eligible/bowlers')
  const [viewMode, setViewMode] = useState('top10')
  const [search, setSearch] = useState('')
  const [sortKey, setSortKey] = useState('Rank')
  const [sortAsc, setSortAsc] = useState(true)
  const [expanded, setExpanded] = useState(null)

  const loading = viewMode === 'top10' ? topLoading : eligLoading
  const error = topError

  if (loading) return <Loading />
  if (error)   return <ErrorBanner msg={error} />

  const rawList = viewMode === 'top10' ? (topData || []) : (eligibleData || [])

  const rows = [...rawList]
    .filter(p => p.player_name?.toLowerCase().includes(search.toLowerCase()))
    .sort((a,b) => {
      const vA = isNaN(+a[sortKey]) ? (a[sortKey] || '') : +a[sortKey]
      const vB = isNaN(+b[sortKey]) ? (b[sortKey] || '') : +b[sortKey]
      if (typeof vA === 'string') {
        return sortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA)
      }
      return sortAsc ? vA - vB : vB - vA
    })

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortAsc(!sortAsc)
    } else {
      setSortKey(key)
      setSortAsc(key === 'Rank' || key === 'player_name' || key === 'press_economy')
    }
  }

  const chartData = (topData||[]).slice(0,10).map(p => ({
    name: p.player_name?.split(' ').slice(-1)[0],
    'Normal Econ':   +fmt(p.norm_economy,2),
    'Pressure Econ': +fmt(p.press_economy,2),
    'Reliability': +fmt(p.reliability_score,1),
  }))

  const headers = [
    { key:'Rank', label:'#' },
    { key:'player_name', label:'Player' },
    { key:'reliability_score', label:'Reliability' },
    { key:'press_economy', label:'Press Econ' },
    { key:'norm_economy', label:'Norm Econ' },
    { key:'econ_suppression', label:'Suppression' },
    { key:'press_wickets', label:'P.Wkts' },
    { key:'press_matches', label:'P.Matches' },
    { key:'press_dot_pct', label:'Press Dot%' },
    { key:'dot_lift', label:'Dot Lift' },
  ]

  return (
    <div className="fade-in-up">
      <PageHeader
        title="Bowlers Intelligence"
        subtitle="Pressure performance rankings for bowlers — identifying wicket-takers who tighten the screws in high-stake overs."
        accent="blue"
      />

      <div style={{ display:'grid', gridTemplateColumns:'2fr 1fr', gap:20, marginBottom:28 }}>
        <div className="glass-card" style={{ padding:24 }}>
          <div style={{ fontWeight:700, marginBottom:16 }}>Normal vs Pressure Economy (RPO) — Top 10</div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chartData} margin={{top:5,right:16,left:0,bottom:5}}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" tick={{ fill:'#64748B', fontSize:11 }} axisLine={false} tickLine={false} />
              <YAxis domain={[0,10]} tick={{ fill:'#64748B', fontSize:11 }} axisLine={false} tickLine={false} label={{ value:'RPO', angle:-90, position:'insideLeft', fill:'#64748B', fontSize:10 }} />
              <Tooltip contentStyle={{ background:'var(--navy-card)', border:'1px solid var(--border)', borderRadius:10 }} labelStyle={{ color:'#fff', fontWeight:600 }} />
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize:11 }} />
              <Bar dataKey="Normal Econ"   fill="#8B5CF6" radius={[4,4,0,0]} />
              <Bar dataKey="Pressure Econ" fill="#22C55E" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="glass-card" style={{ padding:24 }}>
          <div style={{ fontWeight:700, marginBottom:16 }}>Reliability Score — Top 10</div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart layout="vertical"
              data={(topData||[]).slice(0,10).map(p=>({ name:p.player_name?.split(' ').slice(-1)[0], score:+fmt(p.reliability_score,1) }))}
              margin={{top:5,right:16,left:0,bottom:5}}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" domain={[60,100]} tick={{ fill:'#94A3B8', fontSize:10 }} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="name" tick={{ fill:'#CBD5E1', fontSize:11, fontWeight:600 }} axisLine={false} tickLine={false} width={80} />
              <Tooltip contentStyle={{ background:'var(--navy-card)', border:'1px solid var(--border)', borderRadius:10 }} />
              <Bar dataKey="score" radius={[0,4,4,0]} fill="#0EA5E9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-card" style={{ padding:0, overflow:'hidden' }}>
        <div style={{ padding:'18px 24px', borderBottom:'1px solid var(--border)', display:'flex', justifyContent:'space-between', alignItems:'center', flexWrap:'wrap', gap:12 }}>
          <div style={{ display:'flex', alignItems:'center', gap:14 }}>
            <div style={{ fontWeight:700, fontSize:'1.05rem', color:'#FFFFFF' }}>
              {viewMode === 'top10' ? '🏆 Official Top 10 Bowler Rankings' : `🎳 All Qualified Bowlers (${rows.length})`}
            </div>
            <div style={{ display:'flex', gap:6, background:'rgba(255,255,255,0.05)', padding:3, borderRadius:8 }}>
              <button
                onClick={() => { setViewMode('top10'); setSortKey('Rank'); setSortAsc(true); }}
                style={{
                  border:'none', borderRadius:6, padding:'5px 12px', fontSize:'0.75rem', fontWeight:600, cursor:'pointer',
                  background: viewMode === 'top10' ? 'var(--blue)' : 'transparent',
                  color: viewMode === 'top10' ? '#fff' : 'var(--text-muted)'
                }}
              >
                Top 10
              </button>
              <button
                onClick={() => { setViewMode('all'); setSortKey('reliability_score'); setSortAsc(false); }}
                style={{
                  border:'none', borderRadius:6, padding:'5px 12px', fontSize:'0.75rem', fontWeight:600, cursor:'pointer',
                  background: viewMode === 'all' ? 'var(--pink)' : 'transparent',
                  color: viewMode === 'all' ? '#fff' : 'var(--text-muted)'
                }}
              >
                All 186 Bowlers
              </button>
            </div>
          </div>
          <input
            placeholder="🔍 Search bowler by name…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{
              background:'rgba(255,255,255,0.05)', border:'1px solid var(--border)',
              borderRadius:8, padding:'8px 14px', color:'var(--text-primary)',
              fontSize:'0.82rem', outline:'none', width:220
            }}
          />
        </div>
        <div style={{ overflowX:'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                {headers.map(h => (
                  <th key={h.key} onClick={() => handleSort(h.key)} style={{ cursor:'pointer', userSelect:'none', whiteSpace:'nowrap' }}>
                    {h.label} {sortKey === h.key ? (sortAsc ? '▲' : '▼') : ''}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((p,i) => (
                <BowlerRow
                  key={p.player_id}
                  player={p}
                  rank={viewMode === 'top10' ? (+p.Rank || i+1) : (i+1)}
                  expanded={expanded===p.player_id}
                  onToggle={()=>setExpanded(expanded===p.player_id?null:p.player_id)}
                />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
