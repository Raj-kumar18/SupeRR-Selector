import { useState } from 'react'
import { useApi, Loading, ErrorBanner, PageHeader, Avatar, NationalityFlag, StatChip, fmt } from '../components/shared'

/*
  Category strings MUST match the actual values in rr_recruitment_batters.csv
  and rr_recruitment_bowlers.csv exactly.

  Verified from data:
    - 'Historical Rajasthan Royals'  (23 batters, 26 bowlers)
    - 'Other IPL Franchise'          (120 batters, 110 bowlers)
    - 'International-Only'           (55 batters, 50 bowlers)
*/
const CAT_COLORS = {
  'Historical Rajasthan Royals': {
    bg:     'rgba(234,26,127,0.12)',
    border: 'rgba(234,26,127,0.4)',
    color:  'var(--pink)',
    badge:  '🏏 RR Historical',
  },
  'Other IPL Franchise': {
    bg:     'rgba(14,165,233,0.08)',
    border: 'rgba(14,165,233,0.3)',
    color:  'var(--blue)',
    badge:  '🏟 Other IPL',
  },
  'International-Only': {
    bg:     'rgba(139,92,246,0.08)',
    border: 'rgba(139,92,246,0.3)',
    color:  '#8B5CF6',
    badge:  '🌍 T20I Only',
  },
  default: {
    bg:     'rgba(255,215,0,0.06)',
    border: 'rgba(255,215,0,0.25)',
    color:  'var(--gold)',
    badge:  '⭐ Prospect',
  },
}

function getCat(cat) {
  return CAT_COLORS[cat] || CAT_COLORS.default
}

function PlayerCard({ p, type }) {
  const [open, setOpen] = useState(false)
  const isBatter = type === 'batter'
  const c = getCat(p.category)

  return (
    <div
      style={{
        background: c.bg,
        border: `1px solid ${c.border}`,
        borderRadius: 16,
        padding: '18px 20px',
        cursor: 'pointer',
        transition: 'transform 0.2s, box-shadow 0.2s',
        position: 'relative',
        overflow: 'hidden',
      }}
      onClick={() => setOpen(!open)}
      onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = `0 8px 24px ${c.border}` }}
      onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none' }}
    >
      {/* Category badge */}
      <div style={{
        position: 'absolute', top: 12, right: 14,
        fontSize: '0.6rem', fontWeight: 700, letterSpacing: '0.08em',
        color: c.color, background: c.bg,
        border: `1px solid ${c.border}`, borderRadius: 20,
        padding: '2px 8px',
      }}>
        {c.badge}
      </div>

      {/* Player header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
        <Avatar name={p.player_name} size={46} />
        <div>
          <div style={{ fontWeight: 700, fontSize: '0.92rem', paddingRight: 90 }}>{p.player_name}</div>
          <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginTop: 3 }}>
            <NationalityFlag country={p.team_name} /> {p.team_name}
          </div>
        </div>
      </div>

      {/* Key stats row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 10 }}>
        <div style={{ textAlign: 'center', background: 'rgba(255,215,0,0.06)', borderRadius: 8, padding: '8px 4px' }}>
          <div style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--gold)', lineHeight: 1 }}>
            {fmt(p.reliability_score, 1)}%
          </div>
          <div style={{ fontSize: '0.6rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: 2 }}>Reliability</div>
        </div>
        <StatChip
          label={isBatter ? 'Press SR' : 'Press Econ (RPO)'}
          value={isBatter ? fmt(p.press_strike_rate, 1) : fmt(p.press_economy, 2)}
          color="var(--pink)"
        />
        <StatChip label="P.Matches" value={p.press_matches} />
      </div>

      {/* Expandable detail */}
      {open && (
        <div style={{ marginTop: 14, borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: 14 }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: 10 }}>
            <StatChip label="Historical Teams" value={p.historical_teams || '—'} />
            <StatChip label="IPL Franchise(s)" value={p.ipl_franchises || '—'} color="var(--blue)" />
            <StatChip
              label={isBatter ? 'IPL Press SR' : 'IPL Press Econ'}
              value={isBatter ? (fmt(p.ipl_p_sr, 1) || '—') : (fmt(p.ipl_p_econ, 2) || '—')}
              color="var(--gold)"
            />
            <StatChip
              label={isBatter ? 'T20I Press SR' : 'T20I Press Econ'}
              value={isBatter ? (fmt(p.t20i_p_sr, 1) || '—') : (fmt(p.t20i_p_econ, 2) || '—')}
              color="var(--green)"
            />
            {isBatter && (
              <>
                <StatChip label="Normal SR"       value={fmt(p.norm_strike_rate, 1)} />
                <StatChip label="Press Avg"        value={fmt(p.press_average, 1)} color="var(--blue)" />
                <StatChip label="Batting Role"     value={p.batting_role || '—'} />
                <StatChip label="Median Bat Pos"   value={p.median_bat_pos ? `#${Number(p.median_bat_pos).toFixed(0)}` : '—'} />
              </>
            )}
            {!isBatter && (
              <>
                <StatChip label="Normal Econ (RPO)" value={fmt(p.norm_economy, 2)} />
                <StatChip label="Press Wickets"      value={p.press_wickets} color="var(--pink)" />
                <StatChip label="Confidence Factor"  value={fmt(p.confidence_factor, 2)} />
                <StatChip label="Press Legal Balls"  value={p.press_legal_balls} />
              </>
            )}
          </div>
        </div>
      )}

      {/* Expand hint */}
      <div style={{ textAlign: 'center', marginTop: 10, fontSize: '0.65rem', color: 'var(--text-muted)' }}>
        {open ? '▲ collapse' : '▼ tap for details'}
      </div>
    </div>
  )
}

export default function RecruitmentMatrix() {
  const { data, loading, error } = useApi('/api/recruitment')
  const [tab, setTab] = useState('batters')
  const [catFilter, setCatFilter] = useState('All')
  const [search, setSearch] = useState('')

  if (loading) return <Loading />
  if (error)   return <ErrorBanner msg={error} />

  const players = tab === 'batters' ? (data?.batters || []) : (data?.bowlers || [])

  /* Dynamic category list from actual data */
  const cats = ['All', ...new Set(players.map(p => p.category).filter(Boolean))]

  const filtered = players
    .filter(p => catFilter === 'All' || p.category === catFilter)
    .filter(p => p.player_name?.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => +b.reliability_score - +a.reliability_score)

  const batCount = data?.batters?.length || 0
  const bowCount = data?.bowlers?.length || 0

  return (
    <div className="fade-in-up">
      <PageHeader
        title="RR Recruitment Matrix"
        subtitle="Layer 2 enriched recruitment intelligence — historical team affiliations, format splits, and pressure reliability for auction targeting."
        accent="gold"
      />

      {/* Disclaimer */}
      <div style={{
        background: 'rgba(255,215,0,0.06)',
        border: '1px solid rgba(255,215,0,0.25)',
        borderRadius: 12, padding: '14px 18px', marginBottom: 24,
        fontSize: '0.82rem', color: '#FDE68A', lineHeight: 1.7,
      }}>
        ⚠️ <strong>Important:</strong> Historical team associations are based on <code>playing_eleven.csv</code> and
        <code> competition_team_player_mapping.csv</code> from the supplied dataset only.
        Availability for IPL 2027 auction must be verified against official BCCI retention lists, RTM cards,
        and player contracts. These are analytical pressure-performance recommendations, not confirmed auction participants.
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
        {[
          { key: 'batters', label: '🏏 Batters', count: batCount },
          { key: 'bowlers', label: '🎳 Bowlers', count: bowCount },
        ].map(t => (
          <button
            key={t.key}
            onClick={() => { setTab(t.key); setCatFilter('All') }}
            style={{
              padding: '8px 20px', borderRadius: 8,
              border: `1px solid ${tab === t.key ? 'rgba(234,26,127,0.4)' : 'var(--border)'}`,
              background: tab === t.key
                ? 'linear-gradient(135deg,rgba(234,26,127,0.3),rgba(14,165,233,0.2))'
                : 'transparent',
              color: tab === t.key ? '#fff' : 'var(--text-muted)',
              cursor: 'pointer', fontWeight: tab === t.key ? 600 : 400,
              fontSize: '0.875rem', transition: 'all 0.2s',
            }}
          >
            {t.label} <span style={{ opacity: 0.6, fontSize: '0.8rem' }}>({t.count})</span>
          </button>
        ))}
      </div>

      {/* Category filters */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap', alignItems: 'center' }}>
        {cats.map(c => {
          const style = c === 'All' ? { color: 'var(--gold)', bg: 'rgba(255,215,0,0.06)', border: 'rgba(255,215,0,0.25)' }
            : { color: getCat(c).color, bg: getCat(c).bg, border: getCat(c).border }
          const active = catFilter === c
          return (
            <button
              key={c}
              onClick={() => setCatFilter(c)}
              style={{
                padding: '5px 14px', borderRadius: 20,
                border: `1px solid ${active ? style.border : 'var(--border)'}`,
                background: active ? style.bg : 'transparent',
                color: active ? style.color : 'var(--text-muted)',
                cursor: 'pointer', fontSize: '0.75rem',
                fontWeight: active ? 600 : 400, transition: 'all 0.2s',
              }}
            >
              {c}
              {c !== 'All' && (
                <span style={{ marginLeft: 5, opacity: 0.6 }}>
                  ({players.filter(p => p.category === c).length})
                </span>
              )}
            </button>
          )
        })}
        <input
          placeholder="🔍 Search player…"
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{
            marginLeft: 'auto', background: 'rgba(255,255,255,0.05)',
            border: '1px solid var(--border)', borderRadius: 8,
            padding: '6px 14px', color: 'var(--text-primary)',
            fontSize: '0.8rem', outline: 'none', width: 200,
            flexShrink: 0,
          }}
        />
      </div>

      {/* Results count */}
      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 14 }}>
        Showing {filtered.length} players · sorted by Reliability Score ↓
      </div>

      {/* Player grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
        gap: 16,
      }}>
        {filtered.map(p => (
          <PlayerCard key={p.player_id || p.player_name} p={p} type={tab === 'batters' ? 'batter' : 'bowler'} />
        ))}
        {filtered.length === 0 && (
          <div style={{
            gridColumn: '1/-1', padding: 48, textAlign: 'center',
            color: 'var(--text-muted)', background: 'var(--glass)',
            borderRadius: 16, border: '1px solid var(--border)',
          }}>
            No players match the current filter.
          </div>
        )}
      </div>
    </div>
  )
}
