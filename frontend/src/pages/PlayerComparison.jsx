import { useState } from 'react'
import { useApi, Loading, ErrorBanner, PageHeader, Avatar, NationalityFlag, StatChip, fmt } from '../components/shared'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts'

function PlayerSelector({ players, selected, onSelect, label }) {
  const [query, setQuery] = useState('')
  const filtered = (players || []).filter(p => p.player_name?.toLowerCase().includes(query.toLowerCase()))

  return (
    <div style={{ background:'rgba(255,255,255,0.03)', border:'1px solid var(--border)', borderRadius:12, padding:14 }}>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:8 }}>
        <div style={{ fontSize:'0.75rem', color:'var(--text-muted)', textTransform:'uppercase', letterSpacing:'0.08em', fontWeight:700 }}>
          {label}
        </div>
        <div style={{ fontSize:'0.7rem', color:'var(--text-muted)' }}>
          {filtered.length} players
        </div>
      </div>
      <div style={{ position:'relative', marginBottom:8 }}>
        <input
          type="text"
          placeholder="🔍 Type player name to filter..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          style={{
            width:'100%',
            background:'rgba(255,255,255,0.06)',
            border:'1px solid rgba(255,255,255,0.15)',
            borderRadius:8,
            padding:'8px 12px',
            color:'#FFFFFF',
            fontSize:'0.85rem',
            outline:'none',
            boxSizing:'border-box',
          }}
        />
        {query && (
          <button
            onClick={() => setQuery('')}
            style={{
              position:'absolute', right:8, top:'50%', transform:'translateY(-50%)',
              background:'transparent', border:'none', color:'var(--text-muted)', cursor:'pointer', fontSize:'0.8rem'
            }}
          >
            ✕
          </button>
        )}
      </div>
      <select
        value={selected}
        onChange={e => onSelect(e.target.value)}
        style={{
          width:'100%',
          background:'#0F172A',
          border:'1px solid rgba(255,255,255,0.25)',
          borderRadius:8,
          padding:'10px 12px',
          color:'#FFFFFF',
          fontSize:'0.92rem',
          fontWeight:600,
          outline:'none',
          cursor:'pointer',
        }}
      >
        <option value="" style={{ background:'#0F172A', color:'#94A3B8' }}>— Select from list ({filtered.length}) —</option>
        {filtered.map(p => (
          <option key={p.player_id} value={p.player_id} style={{ background:'#0F172A', color:'#FFFFFF', fontWeight:600, padding:'6px' }}>
            {p.player_name} ({fmt(p.reliability_score,1)}% Reliability)
          </option>
        ))}
      </select>
    </div>
  )
}

function CompareRadar({ p1, p2, type }) {
  const isBatter = type === 'batter'
  if (!p1 && !p2) return null

  const keys = isBatter
    ? ['reliability_score','press_strike_rate','press_average','press_boundary_pct','sr_lift','confidence_factor']
    : ['reliability_score','press_economy','press_dot_pct','dot_lift','boundary_prevention','confidence_factor']
  const labels = isBatter
    ? ['Reliability','Press SR','Press Avg','Boundary%','SR Lift','Confidence']
    : ['Reliability','Economy','Dot%','Dot Lift','Boundary Prev.','Confidence']

  // Normalise values to 0-100
  const ranges = {
    reliability_score: [70,100],
    press_strike_rate: [100,250], press_average: [10,60],
    press_boundary_pct: [15,45], sr_lift: [0,60], confidence_factor: [0,1],
    press_economy: [4,10], press_dot_pct: [30,60], dot_lift: [0,15], boundary_prevention: [0,15],
  }
  const norm = (val, key) => {
    const [lo,hi] = ranges[key]||[0,100]
    // For economy, lower is better → invert
    const v = key === 'press_economy' ? (1 - (+val-lo)/(hi-lo))*100 : ((+val-lo)/(hi-lo))*100
    return Math.min(100, Math.max(0, +v.toFixed(1)))
  }

  const data = keys.map((k,i) => ({
    subject: labels[i],
    ...(p1 ? { [p1.player_name?.split(' ').slice(-1)[0]]: norm(p1[k],k) } : {}),
    ...(p2 ? { [p2.player_name?.split(' ').slice(-1)[0]]: norm(p2[k],k) } : {}),
  }))

  return (
    <ResponsiveContainer width="100%" height={320}>
      <RadarChart data={data}>
        <PolarGrid stroke="rgba(255,255,255,0.1)" />
        <PolarAngleAxis dataKey="subject" tick={{ fill:'#94A3B8', fontSize:11 }} />
        <PolarRadiusAxis angle={90} domain={[0,100]} tick={{ fill:'#64748B', fontSize:9 }} />
        {p1 && <Radar name={p1.player_name} dataKey={p1.player_name?.split(' ').slice(-1)[0]} stroke="#EA1A7F" fill="#EA1A7F" fillOpacity={0.2} />}
        {p2 && <Radar name={p2.player_name} dataKey={p2.player_name?.split(' ').slice(-1)[0]} stroke="#0EA5E9" fill="#0EA5E9" fillOpacity={0.2} />}
        <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize:11 }} />
        <Tooltip contentStyle={{ background:'var(--navy-card)', border:'1px solid var(--border)', borderRadius:10 }} />
      </RadarChart>
    </ResponsiveContainer>
  )
}

function StatRow({ label, v1, v2, higherBetter=true }) {
  const n1 = +v1||0, n2 = +v2||0
  const better1 = higherBetter ? n1 >= n2 : n1 <= n2
  return (
    <div style={{ display:'grid', gridTemplateColumns:'1fr auto 1fr', gap:12, alignItems:'center', padding:'10px 0', borderBottom:'1px solid rgba(255,255,255,0.05)' }}>
      <div style={{ textAlign:'right', fontWeight: better1?800:500, color: better1?'#F43FA0':'#94A3B8', fontSize:'0.92rem' }}>
        {fmt(v1,2)} {better1 && '✓'}
      </div>
      <div style={{ fontSize:'0.72rem', color:'#CBD5E1', textAlign:'center', textTransform:'uppercase', letterSpacing:'0.06em', minWidth:130, fontWeight:600 }}>{label}</div>
      <div style={{ fontWeight: !better1?800:500, color: !better1?'#38BDF8':'#94A3B8', fontSize:'0.92rem' }}>
        {!better1 && '✓ '}{fmt(v2,2)}
      </div>
    </div>
  )
}

export default function PlayerComparison() {
  const { data: eligibleBatters } = useApi('/api/eligible/batters')
  const { data: eligibleBowlers } = useApi('/api/eligible/bowlers')
  const { data: topBatters } = useApi('/api/overall/batters')
  const { data: topBowlers } = useApi('/api/overall/bowlers')
  const [type, setType] = useState('batter')
  const [id1, setId1] = useState('47') // Default Virat Kohli
  const [id2, setId2] = useState('1699') // Default Suryakumar Yadav

  const battersList = (eligibleBatters && eligibleBatters.length > 0) ? eligibleBatters : (topBatters || [])
  const bowlersList = (eligibleBowlers && eligibleBowlers.length > 0) ? eligibleBowlers : (topBowlers || [])

  const pool = type === 'batter' ? battersList : bowlersList
  const p1 = pool.find(p => String(p.player_id) === String(id1))
  const p2 = pool.find(p => String(p.player_id) === String(id2))

  const isBatter = type === 'batter'

  return (
    <div className="fade-in-up">
      <PageHeader
        title="Player Comparison"
        subtitle="Head-to-head pressure performance comparison between any two players."
        accent="blue"
      />

      {/* Controls */}
      <div style={{ display:'flex', gap:12, marginBottom:24, alignItems:'center', flexWrap:'wrap' }}>
        {['batter','bowler'].map(t => (
          <button key={t} onClick={()=>{
            setType(t)
            if (t === 'batter') {
              setId1('47')
              setId2('1699')
            } else {
              setId1('3644') // Kuldeep Yadav
              setId2('781')  // Sunil Narine
            }
          }} style={{
            padding:'10px 24px', borderRadius:10, border:'1px solid var(--border)',
            background: type===t ? 'linear-gradient(135deg,rgba(234,26,127,0.4),rgba(14,165,233,0.3))' : 'rgba(255,255,255,0.03)',
            color: type===t ? '#fff' : 'var(--text-muted)',
            cursor:'pointer', fontWeight: type===t ? 700 : 500, fontSize:'0.92rem',
            borderColor: type===t ? 'var(--pink)' : 'var(--border)',
            boxShadow: type===t ? '0 0 15px rgba(234,26,127,0.25)' : 'none',
            transition:'all 0.2s',
          }}>
            {t === 'batter' ? '🏏 Batters' : '🎳 Bowlers'}
          </button>
        ))}
        <span style={{ fontSize:'0.8rem', color:'var(--text-muted)', marginLeft:'auto' }}>
          Comparing {pool.length} qualified players
        </span>
      </div>

      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16, marginBottom:24 }}>
        <PlayerSelector players={pool} selected={id1} onSelect={setId1} label="Player 1 (Pink)" />
        <PlayerSelector players={pool} selected={id2} onSelect={setId2} label="Player 2 (Blue)" />
      </div>

      {(!p1 && !p2) && (
        <div style={{ padding:40, textAlign:'center', color:'var(--text-muted)', background:'var(--glass)', borderRadius:16, border:'1px solid var(--border)' }}>
          Select two players above to compare their pressure performance.
        </div>
      )}

      {(p1 || p2) && (
        <>
          {/* Headers */}
          <div style={{ display:'grid', gridTemplateColumns:'1fr auto 1fr', gap:12, marginBottom:24 }}>
            {p1 ? (
              <div className="glass-card" style={{ padding:20, display:'flex', alignItems:'center', gap:14, borderColor:'rgba(244,63,160,0.4)', background:'rgba(244,63,160,0.06)' }}>
                <Avatar name={p1.player_name} size={56} />
                <div>
                  <div style={{ fontWeight:800, fontSize:'1.15rem', color:'#FFFFFF' }}>{p1.player_name}</div>
                  <div style={{ fontSize:'0.8rem', color:'#CBD5E1', marginTop:2 }}><NationalityFlag country={p1.team_name} /> {p1.team_name}</div>
                  <div style={{ color:'#F43FA0', fontWeight:800, fontSize:'1.3rem', marginTop:4 }}>{fmt(p1.reliability_score,1)}%</div>
                </div>
              </div>
            ) : <div />}
            <div style={{ display:'flex', alignItems:'center', justifyContent:'center', color:'var(--gold)', fontWeight:900, fontSize:'1.4rem' }}>VS</div>
            {p2 ? (
              <div className="glass-card" style={{ padding:20, display:'flex', alignItems:'center', gap:14, borderColor:'rgba(56,189,248,0.4)', background:'rgba(56,189,248,0.06)' }}>
                <Avatar name={p2.player_name} size={56} />
                <div>
                  <div style={{ fontWeight:800, fontSize:'1.15rem', color:'#FFFFFF' }}>{p2.player_name}</div>
                  <div style={{ fontSize:'0.8rem', color:'#CBD5E1', marginTop:2 }}><NationalityFlag country={p2.team_name} /> {p2.team_name}</div>
                  <div style={{ color:'#38BDF8', fontWeight:800, fontSize:'1.3rem', marginTop:4 }}>{fmt(p2.reliability_score,1)}%</div>
                </div>
              </div>
            ) : <div />}
          </div>

          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20 }}>
            {/* Radar */}
            <div className="glass-card" style={{ padding:24 }}>
              <div style={{ fontWeight:700, marginBottom:16 }}>Pressure Performance Radar</div>
              <CompareRadar p1={p1} p2={p2} type={type} />
            </div>

            {/* Stat by stat */}
            <div className="glass-card" style={{ padding:24 }}>
              <div style={{ fontWeight:700, marginBottom:16 }}>Head-to-Head Stats</div>
              <div style={{ display:'grid', gridTemplateColumns:'1fr auto 1fr', gap:0, borderBottom:'1px solid rgba(255,255,255,0.1)', paddingBottom:10 }}>
                <div style={{ textAlign:'right', fontSize:'0.95rem', color:'#F43FA0', fontWeight:800 }}>{p1?.player_name || '—'}</div>
                <div style={{ padding:'0 10px', fontSize:'0.75rem', color:'var(--text-muted)', fontWeight:700 }}>VS</div>
                <div style={{ fontSize:'0.95rem', color:'#38BDF8', fontWeight:800 }}>{p2?.player_name || '—'}</div>
              </div>
              <StatRow label="Reliability %" v1={p1?.reliability_score} v2={p2?.reliability_score} />
              {isBatter ? <>
                <StatRow label="Pressure SR"        v1={p1?.press_strike_rate}  v2={p2?.press_strike_rate} />
                <StatRow label="Normal SR"           v1={p1?.norm_strike_rate}   v2={p2?.norm_strike_rate} />
                <StatRow label="SR Lift (pts)"       v1={p1?.sr_lift}            v2={p2?.sr_lift} />
                <StatRow label="Pressure Avg"        v1={p1?.press_average}      v2={p2?.press_average} />
                <StatRow label="Normal Avg"          v1={p1?.norm_average}       v2={p2?.norm_average} />
                <StatRow label="Press Boundary%"     v1={p1?.press_boundary_pct} v2={p2?.press_boundary_pct} />
                <StatRow label="Normal Boundary%"    v1={p1?.norm_boundary_pct}  v2={p2?.norm_boundary_pct} />
                <StatRow label="Boundary Lift%"      v1={p1?.boundary_lift}      v2={p2?.boundary_lift} />
                <StatRow label="Press Dot%"          v1={p1?.press_dot_pct}      v2={p2?.press_dot_pct} higherBetter={false} />
                <StatRow label="Dot Reduction%"      v1={p1?.dot_reduction}      v2={p2?.dot_reduction} />
                <StatRow label="Pressure Balls"      v1={p1?.press_balls_faced}  v2={p2?.press_balls_faced} />
              </> : <>
                <StatRow label="Press Economy(RPO)"  v1={p1?.press_economy}     v2={p2?.press_economy} higherBetter={false} />
                <StatRow label="Normal Economy"      v1={p1?.norm_economy}      v2={p2?.norm_economy}  higherBetter={false} />
                <StatRow label="Econ Suppression"    v1={p1?.econ_suppression}  v2={p2?.econ_suppression} />
                <StatRow label="Press Bowling SR"    v1={p1?.press_strike_rate} v2={p2?.press_strike_rate} higherBetter={false} />
                <StatRow label="Press Wickets"       v1={p1?.press_wickets}     v2={p2?.press_wickets} />
                <StatRow label="Press Dot%"          v1={p1?.press_dot_pct}     v2={p2?.press_dot_pct} />
                <StatRow label="Dot Lift%"           v1={p1?.dot_lift}          v2={p2?.dot_lift} />
                <StatRow label="Press Boundary Conc%" v1={p1?.press_boundary_conceded_pct} v2={p2?.press_boundary_conceded_pct} higherBetter={false} />
                <StatRow label="Boundary Prevention" v1={p1?.boundary_prevention} v2={p2?.boundary_prevention} />
                <StatRow label="Press Legal Balls"   v1={p1?.press_legal_balls} v2={p2?.press_legal_balls} />
              </>}
              <StatRow label="Confidence Factor" v1={p1?.confidence_factor} v2={p2?.confidence_factor} />
              <StatRow label="Press Matches"     v1={p1?.press_matches}     v2={p2?.press_matches} />
            </div>
          </div>
        </>
      )}
    </div>
  )
}
