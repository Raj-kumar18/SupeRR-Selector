import { useApi, Loading, ErrorBanner, PageHeader, RankBadge, StatChip, Avatar, NationalityFlag, fmt } from '../components/shared'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts'

const KPI_COLORS = [
  { bg:'rgba(234,26,127,0.12)', border:'rgba(234,26,127,0.4)', accent:'var(--pink)',  icon:'🎯' },
  { bg:'rgba(14,165,233,0.12)', border:'rgba(14,165,233,0.4)', accent:'var(--blue)',  icon:'⚡' },
  { bg:'rgba(255,215,0,0.10)',  border:'rgba(255,215,0,0.4)',  accent:'var(--gold)',  icon:'🏆' },
  { bg:'rgba(139,92,246,0.12)', border:'rgba(139,92,246,0.4)', accent:'#8B5CF6',     icon:'🔥' },
  { bg:'rgba(34,197,94,0.12)',  border:'rgba(34,197,94,0.4)',  accent:'var(--green)', icon:'🏏' },
  { bg:'rgba(249,115,22,0.12)', border:'rgba(249,115,22,0.4)', accent:'#F97316',     icon:'🎳' },
]

function KpiCard({ label, value, style, icon }) {
  return (
    <div style={{
      background: style.bg, border: `1px solid ${style.border}`,
      borderRadius: 16, padding: '20px 24px',
      display:'flex', alignItems:'center', gap:16,
      transition:'transform 0.2s, box-shadow 0.2s',
      cursor:'default',
    }}
    onMouseEnter={e=>e.currentTarget.style.transform='translateY(-2px)'}
    onMouseLeave={e=>e.currentTarget.style.transform='translateY(0)'}
    >
      <div style={{ fontSize:32 }}>{icon}</div>
      <div>
        <div style={{ fontSize:'0.7rem', color:'var(--text-muted)', textTransform:'uppercase', letterSpacing:'0.1em', marginBottom:4 }}>{label}</div>
        <div style={{ fontSize:'1.8rem', fontWeight:800, color: style.accent, lineHeight:1 }}>
          {typeof value === 'number' ? value.toLocaleString() : value}
        </div>
      </div>
    </div>
  )
}

function TopPlayerCard({ player, rank, type }) {
  const isBatter = type === 'batter'
  return (
    <div style={{
      background:'var(--glass)', border:'1px solid var(--border)', borderRadius:16,
      padding:'20px', display:'flex', flexDirection:'column', gap:14,
      position:'relative', overflow:'hidden',
      transition:'transform 0.2s, border-color 0.2s',
    }}
    onMouseEnter={e=>{e.currentTarget.style.transform='translateY(-3px)'; e.currentTarget.style.borderColor='rgba(234,26,127,0.4)'}}
    onMouseLeave={e=>{e.currentTarget.style.transform='translateY(0)'; e.currentTarget.style.borderColor='var(--border)'}}
    >
      {/* Background rank number */}
      <div style={{ position:'absolute', right:12, top:8, fontSize:'5rem', fontWeight:900, color:'rgba(255,255,255,0.03)', lineHeight:1 }}>#{rank}</div>

      <div style={{ display:'flex', alignItems:'center', gap:12 }}>
        <div style={{ position:'relative' }}>
          <Avatar name={player.player_name} size={52} />
          <div style={{ position:'absolute', bottom:-2, right:-2 }}><RankBadge rank={rank} /></div>
        </div>
        <div>
          <div style={{ fontWeight:700, fontSize:'0.95rem' }}>{player.player_name}</div>
          <div style={{ fontSize:'0.75rem', color:'var(--text-muted)', marginTop:2 }}>
            <NationalityFlag country={player.team_name} /> {player.team_name}
          </div>
        </div>
      </div>

      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:12 }}>
        <StatChip label="Reliability" value={fmt(player.reliability_score,1)+'%'} color="var(--gold)" />
        <StatChip label={isBatter ? "Press SR" : "Press Econ"} value={isBatter ? fmt(player.press_strike_rate,1) : fmt(player.press_economy,2)} color="var(--pink)" />
        <StatChip label="Press Matches" value={player.press_matches} color="var(--blue)" />
      </div>

      <div style={{ background:'rgba(255,255,255,0.03)', borderRadius:8, padding:'8px 12px', fontSize:'0.72rem', color:'var(--text-muted)' }}>
        {isBatter
          ? `SR Lift: +${fmt(player.sr_lift,1)}% | Boundary Lift: +${fmt(player.boundary_lift,1)}%`
          : `Economy Suppression: ${fmt(player.econ_suppression,2)} | Dot Lift: +${fmt(player.dot_lift,1)}%`
        }
      </div>
    </div>
  )
}

function PressureCompareChart({ batters }) {
  if (!batters || batters.length === 0) return null
  const data = batters.slice(0,10).map((b, i) => ({
    name: b.player_name?.split(' ').slice(-1)[0],
    fullName: b.player_name,
    rank: i + 1,
    'Normal SR': +fmt(b.norm_strike_rate,1),
    'Pressure SR': +fmt(b.press_strike_rate,1),
    'SR Lift': +fmt(b.sr_lift,1),
    reliability: +fmt(b.reliability_score,1),
  }))
  return (
    <div style={{ marginTop:8 }}>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:12 }}>
        <div style={{ fontSize:'0.75rem', color:'var(--text-muted)', textTransform:'uppercase', letterSpacing:'0.08em', fontWeight:600 }}>
          Top 10 Batters — Normal vs Pressure Strike Rate
        </div>
        <div style={{ fontSize:'0.7rem', color:'var(--pink)', fontWeight:700 }}>
          Ranked 1 to 10
        </div>
      </div>
      <ResponsiveContainer width="100%" height={290}>
        <BarChart data={data} margin={{top:5,right:12,left:-15,bottom:25}}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="name" tick={{ fill:'#94A3B8', fontSize:11 }} interval={0} angle={-25} textAnchor="end" axisLine={false} tickLine={false} />
          <YAxis tick={{ fill:'#94A3B8', fontSize:11 }} domain={[100, 240]} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{ background:'var(--navy-card)', border:'1px solid var(--border)', borderRadius:10, padding:'10px 14px' }}
            labelFormatter={(label, payload) => payload?.[0]?.payload?.fullName ? `#${payload[0].payload.rank} ${payload[0].payload.fullName} (${payload[0].payload.reliability}%)` : label}
            labelStyle={{ color:'#fff', fontWeight:700 }}
            itemStyle={{ color:'var(--text-secondary)' }}
          />
          <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize:11, color:'var(--text-muted)', paddingTop:10 }} />
          <Bar dataKey="Normal SR"   fill="#0EA5E9" radius={[4,4,0,0]} />
          <Bar dataKey="Pressure SR" fill="#EA1A7F" radius={[4,4,0,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

function EconCompareChart({ bowlers }) {
  if (!bowlers || bowlers.length === 0) return null
  const data = bowlers.slice(0,10).map((b, i) => ({
    name: b.player_name?.split(' ').slice(-1)[0],
    fullName: b.player_name,
    rank: i + 1,
    'Normal Econ': +fmt(b.norm_economy,2),
    'Pressure Econ': +fmt(b.press_economy,2),
    reliability: +fmt(b.reliability_score,1),
  }))
  return (
    <div style={{ marginTop:8 }}>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:12 }}>
        <div style={{ fontSize:'0.75rem', color:'var(--text-muted)', textTransform:'uppercase', letterSpacing:'0.08em', fontWeight:600 }}>
          Top 10 Bowlers — Normal vs Pressure Economy (RPO)
        </div>
        <div style={{ fontSize:'0.7rem', color:'var(--blue)', fontWeight:700 }}>
          Ranked 1 to 10
        </div>
      </div>
      <ResponsiveContainer width="100%" height={290}>
        <BarChart data={data} margin={{top:5,right:12,left:-15,bottom:25}}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="name" tick={{ fill:'#94A3B8', fontSize:11 }} interval={0} angle={-25} textAnchor="end" axisLine={false} tickLine={false} />
          <YAxis domain={[0,10]} tick={{ fill:'#94A3B8', fontSize:11 }} axisLine={false} tickLine={false} label={{ value:'RPO', angle:-90, position:'insideLeft', fill:'#64748B', fontSize:10 }} />
          <Tooltip
            contentStyle={{ background:'var(--navy-card)', border:'1px solid var(--border)', borderRadius:10, padding:'10px 14px' }}
            labelFormatter={(label, payload) => payload?.[0]?.payload?.fullName ? `#${payload[0].payload.rank} ${payload[0].payload.fullName} (${payload[0].payload.reliability}%)` : label}
            labelStyle={{ color:'#fff', fontWeight:700 }}
            itemStyle={{ color:'var(--text-secondary)' }}
          />
          <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize:11, color:'var(--text-muted)', paddingTop:10 }} />
          <Bar dataKey="Normal Econ"   fill="#8B5CF6" radius={[4,4,0,0]} />
          <Bar dataKey="Pressure Econ" fill="#22C55E" radius={[4,4,0,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function ExecutiveDashboard() {
  const { data: kpis,    loading: kL } = useApi('/api/kpis')
  const { data: batters, loading: bL } = useApi('/api/overall/batters')
  const { data: bowlers, loading: wL } = useApi('/api/overall/bowlers')

  const kpiDefs = kpis ? [
    { label:'Total Deliveries',    value: kpis.total_deliveries },
    { label:'Legal Deliveries',    value: kpis.legal_deliveries },
    { label:'Matches Analysed',    value: kpis.matches_analyzed },
    { label:'Pressure Deliveries', value: kpis.pressure_deliveries },
    { label:'Qualified Batters',   value: kpis.qualified_batters },
    { label:'Qualified Bowlers',   value: kpis.qualified_bowlers },
  ] : []

  return (
    <div className="fade-in-up">
      {/* Hero */}
      <div style={{
        background:'linear-gradient(135deg,rgba(234,26,127,0.08),rgba(14,165,233,0.06))',
        border:'1px solid var(--border)', borderRadius:20, padding:'32px 36px', marginBottom:28,
        position:'relative', overflow:'hidden',
      }}>
        <div style={{ position:'absolute', right:0, top:0, bottom:0, width:300, background:'radial-gradient(ellipse at right,rgba(234,26,127,0.1),transparent)', pointerEvents:'none' }} />
        <div style={{ fontSize:'0.7rem', color:'var(--pink)', textTransform:'uppercase', letterSpacing:'0.15em', marginBottom:8, fontWeight:600 }}>
          🏆 SupeRR Selector Season 2 — IPL 2027
        </div>
        <h1 style={{ fontFamily:'Rajdhani,sans-serif', fontWeight:700, fontSize:'2.4rem', lineHeight:1.1, marginBottom:10 }}>
          Rajasthan Royals<br/>
          <span className="gradient-text-pink">Auction Intelligence War Room</span>
        </h1>
        <p style={{ color:'var(--text-muted)', maxWidth:580, lineHeight:1.6, fontSize:'0.9rem' }}>
          Ball-by-ball pressure analytics across IPL and T20 International data. 
          Identifying the most reliable performers under high-stakes match situations 
          to shape the RR IPL 2027 auction strategy.
        </p>
        <div style={{ marginTop:20, display:'flex', gap:12, flexWrap:'wrap' }}>
          {['Pressure Definition', 'Reliability Score', 'Layer 1 Rankings', 'RR Recruitment Matrix'].map(tag => (
            <span key={tag} style={{
              background:'rgba(255,255,255,0.05)', border:'1px solid var(--border)',
              borderRadius:20, padding:'4px 12px', fontSize:'0.72rem', color:'var(--text-secondary)'
            }}>{tag}</span>
          ))}
        </div>
      </div>

      {/* KPI Grid */}
      {kL ? <Loading /> : (
        <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))', gap:16, marginBottom:32 }}>
          {kpiDefs.map((k,i) => (
            <KpiCard key={k.label} label={k.label} value={k.value} style={KPI_COLORS[i]} icon={KPI_COLORS[i].icon} />
          ))}
        </div>
      )}

      {/* Charts Row */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:32 }}>
        <div className="glass-card" style={{ padding:24 }}>
          <div style={{ fontWeight:700, marginBottom:4 }}>Batting Pressure Analysis</div>
          {bL ? <Loading /> : <PressureCompareChart batters={batters} />}
        </div>
        <div className="glass-card" style={{ padding:24 }}>
          <div style={{ fontWeight:700, marginBottom:4 }}>Bowling Pressure Analysis</div>
          {wL ? <Loading /> : <EconCompareChart bowlers={bowlers} />}
        </div>
      </div>

      {/* Top 5 Players */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20 }}>
        {/* Batters */}
        <div>
          <div style={{ display:'flex', alignItems:'center', gap:10, marginBottom:16 }}>
            <div style={{ width:4, height:20, background:'var(--pink)', borderRadius:2 }} />
            <div style={{ fontFamily:'Rajdhani,sans-serif', fontWeight:700, fontSize:'1.1rem' }}>Top 5 Batters Under Pressure</div>
          </div>
          {bL ? <Loading /> : (
            <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
              {(batters||[]).slice(0,5).map((p,i) => (
                <TopPlayerCard key={p.player_id} player={p} rank={i+1} type="batter" />
              ))}
            </div>
          )}
        </div>
        {/* Bowlers */}
        <div>
          <div style={{ display:'flex', alignItems:'center', gap:10, marginBottom:16 }}>
            <div style={{ width:4, height:20, background:'var(--blue)', borderRadius:2 }} />
            <div style={{ fontFamily:'Rajdhani,sans-serif', fontWeight:700, fontSize:'1.1rem' }}>Top 5 Bowlers Under Pressure</div>
          </div>
          {wL ? <Loading /> : (
            <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
              {(bowlers||[]).slice(0,5).map((p,i) => (
                <TopPlayerCard key={p.player_id} player={p} rank={i+1} type="bowler" />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
