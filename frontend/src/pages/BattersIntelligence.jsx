import { useState } from 'react'
import { useApi, Loading, ErrorBanner, PageHeader, RankBadge, Avatar, NationalityFlag, StatChip, fmt } from '../components/shared'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter, ZAxis, ReferenceLine
} from 'recharts'

function PlayerRow({ player, rank, expanded, onToggle }) {
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
        <td style={{ color:'var(--pink)', fontWeight:700 }}>{fmt(player.press_strike_rate,1)}</td>
        <td style={{ color:'var(--blue)' }}>{fmt(player.norm_strike_rate,1)}</td>
        <td><span style={{ color:'var(--green)', fontWeight:700 }}>+{fmt(player.sr_lift,1)}</span></td>
        <td style={{ fontWeight:600 }}>{fmt(player.press_average,1)}</td>
        <td>{player.press_matches}</td>
        <td style={{ color:'var(--pink)', fontWeight:600 }}>{fmt(player.press_boundary_pct,1)}%</td>
        <td style={{ color: +player.dot_reduction >= 0 ? '#22C55E' : '#EF4444', fontWeight:600 }}>
          {+player.dot_reduction >= 0 ? '+' : ''}{fmt(player.dot_reduction,1)}%
        </td>
      </tr>
      {expanded && (
        <tr>
          <td colSpan={10} style={{ background:'rgba(234,26,127,0.06)', borderTop:'1px solid rgba(234,26,127,0.2)', borderBottom:'1px solid rgba(234,26,127,0.2)' }}>
            <div style={{ padding:'16px 20px' }}>
              <div style={{ fontSize:'0.75rem', fontWeight:700, color:'var(--pink)', textTransform:'uppercase', letterSpacing:'0.08em', marginBottom:12 }}>
                Detailed Batting Breakdown — {player.player_name}
              </div>
              <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(130px, 1fr))', gap:14 }}>
                <StatChip label="Normal Runs" value={player.norm_runs} />
                <StatChip label="Press Runs" value={player.press_runs} color="var(--pink)" />
                <StatChip label="Press Balls Faced" value={player.press_balls_faced} />
                <StatChip label="Press Fours" value={player.press_fours} />
                <StatChip label="Press Sixes" value={player.press_sixes} color="var(--gold)" />
                <StatChip label="Normal Avg" value={fmt(player.norm_average,1)} />
                <StatChip label="Press Avg" value={fmt(player.press_average,1)} color="var(--blue)" />
                <StatChip label="Norm Boundary %" value={fmt(player.norm_boundary_pct,1)+'%'} />
                <StatChip label="Press Boundary %" value={fmt(player.press_boundary_pct,1)+'%'} color="var(--pink)" />
                <StatChip label="Boundary Lift" value={'+'+fmt(player.boundary_lift,1)+'%'} color="var(--green)" />
                <StatChip label="Norm Dot %" value={fmt(player.norm_dot_pct,1)+'%'} />
                <StatChip label="Press Dot %" value={fmt(player.press_dot_pct,1)+'%'} color="#EF4444" />
                <StatChip label="Dot Reduction" value={fmt(player.dot_reduction,1)+'%'} color="var(--green)" />
                <StatChip label="Confidence Factor" value={fmt(player.confidence_factor,2)} color="var(--gold)" />
              </div>
            </div>
          </td>
        </tr>
      )}
    </>
  )
}

export default function BattersIntelligence() {
  const { data: topData, loading: topLoading, error: topError } = useApi('/api/overall/batters')
  const { data: eligibleData, loading: eligLoading } = useApi('/api/eligible/batters')
  const [viewMode, setViewMode] = useState('top10') // 'top10' or 'all'
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
      // For numerical stats, default to descending except Rank
      setSortAsc(key === 'Rank' || key === 'player_name')
    }
  }

  // Chart: SR lift comparison for top 10
  const chartData = (topData||[]).slice(0,10).map(p => ({
    name: p.player_name?.split(' ').slice(-1)[0],
    fullName: p.player_name,
    'Normal SR': +fmt(p.norm_strike_rate,1),
    'Pressure SR': +fmt(p.press_strike_rate,1),
    'SR Lift': +fmt(p.sr_lift,1),
    'Reliability': +fmt(p.reliability_score,1),
  }))

  const headers = [
    { key:'Rank', label:'#' },
    { key:'player_name', label:'Player' },
    { key:'reliability_score', label:'Reliability' },
    { key:'press_strike_rate', label:'Press SR' },
    { key:'norm_strike_rate', label:'Norm SR' },
    { key:'sr_lift', label:'SR Lift' },
    { key:'press_average', label:'Press Avg' },
    { key:'press_matches', label:'P.Matches' },
    { key:'press_boundary_pct', label:'Bound%' },
    { key:'dot_reduction', label:'Dot Red.' },
  ]

  return (
    <div className="fade-in-up">
      <PageHeader
        title="Batters Intelligence"
        subtitle="Overall pressure performance rankings — all eligible players across IPL & T20I datasets."
        accent="pink"
      />

      {/* Charts */}
      <div style={{ display:'grid', gridTemplateColumns:'2fr 1fr', gap:20, marginBottom:28 }}>
        <div className="glass-card" style={{ padding:24 }}>
          <div style={{ fontWeight:700, marginBottom:16 }}>Normal vs Pressure Strike Rate — Top 10 Batters</div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chartData} margin={{top:5,right:16,left:0,bottom:5}}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" tick={{ fill:'#94A3B8', fontSize:11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill:'#94A3B8', fontSize:11 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background:'var(--navy-card)', border:'1px solid var(--border)', borderRadius:10 }} labelStyle={{ color:'#fff', fontWeight:600 }} />
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize:11 }} />
              <Bar dataKey="Normal SR"   fill="#0EA5E9" radius={[4,4,0,0]} />
              <Bar dataKey="Pressure SR" fill="#EA1A7F" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="glass-card" style={{ padding:24 }}>
          <div style={{ fontWeight:700, marginBottom:16 }}>Reliability Score — Top 10 Batters</div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart layout="vertical" data={[...(topData||[])].slice(0,10).map(p=>({ name:p.player_name?.split(' ').slice(-1)[0], score:+fmt(p.reliability_score,1) }))} margin={{top:5,right:16,left:0,bottom:5}}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" domain={[60,100]} tick={{ fill:'#94A3B8', fontSize:10 }} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="name" tick={{ fill:'#CBD5E1', fontSize:11, fontWeight:600 }} axisLine={false} tickLine={false} width={80} />
              <Tooltip contentStyle={{ background:'var(--navy-card)', border:'1px solid var(--border)', borderRadius:10 }} />
              <Bar dataKey="score" fill="url(#goldGrad)" radius={[0,4,4,0]}>
                <defs>
                  <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#F97316" />
                    <stop offset="100%" stopColor="#FFD700" />
                  </linearGradient>
                </defs>
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Table */}
      <div className="glass-card" style={{ padding:0, overflow:'hidden' }}>
        <div style={{ padding:'18px 24px', borderBottom:'1px solid var(--border)', display:'flex', justifyContent:'space-between', alignItems:'center', flexWrap:'wrap', gap:12 }}>
          <div style={{ display:'flex', alignItems:'center', gap:14 }}>
            <div style={{ fontWeight:700, fontSize:'1.05rem', color:'#FFFFFF' }}>
              {viewMode === 'top10' ? '🏆 Official Top 10 Batter Rankings' : `🏏 All Qualified Batters (${rows.length})`}
            </div>
            <div style={{ display:'flex', gap:6, background:'rgba(255,255,255,0.05)', padding:3, borderRadius:8 }}>
              <button
                onClick={() => { setViewMode('top10'); setSortKey('Rank'); setSortAsc(true); }}
                style={{
                  border:'none', borderRadius:6, padding:'5px 12px', fontSize:'0.75rem', fontWeight:600, cursor:'pointer',
                  background: viewMode === 'top10' ? 'var(--pink)' : 'transparent',
                  color: viewMode === 'top10' ? '#fff' : 'var(--text-muted)'
                }}
              >
                Top 10
              </button>
              <button
                onClick={() => { setViewMode('all'); setSortKey('reliability_score'); setSortAsc(false); }}
                style={{
                  border:'none', borderRadius:6, padding:'5px 12px', fontSize:'0.75rem', fontWeight:600, cursor:'pointer',
                  background: viewMode === 'all' ? 'var(--blue)' : 'transparent',
                  color: viewMode === 'all' ? '#fff' : 'var(--text-muted)'
                }}
              >
                All 198 Batters
              </button>
            </div>
          </div>
          <input
            placeholder="🔍 Search batter by name…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{
              background:'rgba(255,255,255,0.05)', border:'1px solid var(--border)',
              borderRadius:8, padding:'8px 14px', color:'var(--text-primary)',
              fontSize:'0.82rem', outline:'none', width:220,
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
                <PlayerRow
                  key={p.player_id}
                  player={p}
                  rank={viewMode === 'top10' ? (+p.Rank || i+1) : (i+1)}
                  expanded={expanded === p.player_id}
                  onToggle={() => setExpanded(expanded === p.player_id ? null : p.player_id)}
                />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
