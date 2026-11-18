import { PageHeader } from '../components/shared'
import { useState } from 'react'

/* ───────────────────────────────────────────────────────────
   MathEngine.jsx – formulas verified against:
     • pressure_engine.py
     • reliability_model.py
     • batting_metrics.py
     • bowling_metrics.py
     • config.py
   Every constant, weight, threshold and formula shown here
   is copied directly from the Python source code.
─────────────────────────────────────────────────────────── */

function Code({ children }) {
  return (
    <div style={{
      fontFamily: 'monospace',
      background: 'rgba(0,0,0,0.35)',
      border: '1px solid rgba(14,165,233,0.2)',
      borderRadius: 8,
      padding: '12px 16px',
      color: '#93C5FD',
      fontSize: '0.83rem',
      overflowX: 'auto',
      lineHeight: 1.7,
      whiteSpace: 'pre',
      marginBottom: 10,
    }}>
      {children}
    </div>
  )
}

function Formula({ title, children, description }) {
  return (
    <div style={{
      background: 'rgba(255,255,255,0.03)',
      border: '1px solid var(--border)',
      borderRadius: 12,
      padding: 20,
      marginBottom: 14,
    }}>
      <div style={{ fontWeight: 700, color: 'var(--pink)', marginBottom: 8, fontSize: '0.9rem' }}>
        {title}
      </div>
      {children}
      {description && (
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.65, marginTop: 8 }}>
          {description}
        </div>
      )}
    </div>
  )
}

function Callout({ type, children }) {
  const styles = {
    note:    { bg: 'rgba(14,165,233,0.08)',  border: 'rgba(14,165,233,0.3)',  icon: 'ℹ️' },
    warning: { bg: 'rgba(234,179,8,0.08)',   border: 'rgba(234,179,8,0.35)',  icon: '⚠️' },
    caution: { bg: 'rgba(239,68,68,0.08)',   border: 'rgba(239,68,68,0.3)',   icon: '🚨' },
  }
  const s = styles[type] || styles.note
  return (
    <div style={{
      background: s.bg, border: `1px solid ${s.border}`,
      borderRadius: 10, padding: '12px 16px',
      fontSize: '0.82rem', color: 'var(--text-secondary)',
      lineHeight: 1.65, marginBottom: 14,
    }}>
      {s.icon} {children}
    </div>
  )
}

function WeightRow({ metric, weight, note }) {
  return (
    <div style={{
      display: 'grid', gridTemplateColumns: '2fr 80px 1fr',
      gap: 12, padding: '8px 0',
      borderBottom: '1px solid rgba(255,255,255,0.05)',
      alignItems: 'center', fontSize: '0.85rem',
    }}>
      <div style={{ color: 'var(--text-secondary)' }}>{metric}</div>
      <div style={{
        textAlign: 'center', fontWeight: 700, fontFamily: 'monospace',
        color: 'var(--gold)',
        background: 'rgba(255,215,0,0.08)', borderRadius: 6, padding: '2px 0',
      }}>{weight}</div>
      <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{note}</div>
    </div>
  )
}

function Section({ title, accent='blue', children }) {
  const colors = { pink: 'var(--pink)', blue: 'var(--blue)', gold: 'var(--gold)', green: 'var(--green)' }
  return (
    <div style={{ marginBottom: 36 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
        <div style={{ width: 4, height: 20, background: colors[accent], borderRadius: 2 }} />
        <div style={{ fontFamily: 'Rajdhani,sans-serif', fontWeight: 700, fontSize: '1.2rem' }}>{title}</div>
      </div>
      {children}
    </div>
  )
}

function CollapseSection({ title, children }) {
  const [open, setOpen] = useState(false)
  return (
    <div style={{
      border: '1px solid var(--border)', borderRadius: 10,
      marginBottom: 10, overflow: 'hidden',
    }}>
      <div
        onClick={() => setOpen(!open)}
        style={{
          padding: '12px 16px', cursor: 'pointer', display: 'flex',
          justifyContent: 'space-between', alignItems: 'center',
          background: 'rgba(255,255,255,0.03)',
          fontWeight: 600, fontSize: '0.875rem',
        }}
      >
        {title}
        <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{open ? '▲ hide' : '▼ show'}</span>
      </div>
      {open && <div style={{ padding: '16px' }}>{children}</div>}
    </div>
  )
}

export default function MathEngine() {
  return (
    <div className="fade-in-up">
      <PageHeader
        title="Mathematical Engine"
        subtitle="Complete methodology — every formula, threshold and weight is copied directly from the Python source code."
        accent="blue"
      />

      {/* Source verification banner */}
      <div style={{
        background: 'linear-gradient(135deg,rgba(14,165,233,0.1),rgba(139,92,246,0.08))',
        border: '1px solid rgba(14,165,233,0.3)', borderRadius: 12,
        padding: '14px 18px', marginBottom: 28, fontSize: '0.82rem',
        color: 'var(--text-secondary)', lineHeight: 1.7,
      }}>
        📋 <strong style={{ color: 'var(--blue)' }}>Formula Source Verification:</strong>{' '}
        All constants, weights, thresholds and formulas on this page are verified directly from:{' '}
        <code style={{ color: '#93C5FD' }}>pressure_engine.py</code>,{' '}
        <code style={{ color: '#93C5FD' }}>reliability_model.py</code>,{' '}
        <code style={{ color: '#93C5FD' }}>batting_metrics.py</code>,{' '}
        <code style={{ color: '#93C5FD' }}>bowling_metrics.py</code>, and{' '}
        <code style={{ color: '#93C5FD' }}>config.py</code>.
      </div>

      {/* ── 1. DATA COVERAGE ── */}
      <Section title="1. Data Coverage" accent="blue">
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(200px,1fr))',
          gap: 12, marginBottom: 14,
        }}>
          {[
            { label: 'Total Deliveries', value: '200,999' },
            { label: 'Legal Deliveries', value: '192,445' },
            { label: 'Matches Analysed', value: '867' },
            { label: 'High-Pressure Deliveries', value: '48,324 (24.0%)' },
            { label: 'IPL Seasons', value: 'IPL 2022–2026 (5 seasons, 371 matches)' },
            { label: 'T20I Data', value: '134 bilateral T20I series (482 matches)' },
          ].map(d => (
            <div key={d.label} style={{
              background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border)',
              borderRadius: 10, padding: '12px 14px',
            }}>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 4 }}>{d.label}</div>
              <div style={{ fontWeight: 700, color: 'var(--gold)', fontSize: '0.9rem' }}>{d.value}</div>
            </div>
          ))}
        </div>
        <Callout type="warning">
          <strong>No T20 World Cup data:</strong> The supplied dataset contains only bilateral T20I series and IPL seasons (2022–2026).
          ICC T20 World Cups (2022, 2024) are absent. Rankings are therefore based on bilateral T20I and IPL pressure alone.
          Tournament-specialist performances (e.g. World Cup final scenarios) are not captured in these rankings.
        </Callout>
        <Callout type="note">
          "Other T20" category: 2 Asia Cup competitions (Emerging Teams 2024 and Rising Stars 2025) containing 30 matches
          are classified separately and excluded from the IPL / T20I format splits.
        </Callout>
      </Section>

      {/* ── 2. PRESSURE DEFINITION ── */}
      <Section title="2. Pressure Index – Continuous Composite Model" accent="pink">
        <div style={{ background: 'rgba(234,26,127,0.06)', border: '1px solid rgba(234,26,127,0.25)', borderRadius: 12, padding: 20, marginBottom: 14, fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.75 }}>
          <p>
            Pressure is quantified as a <strong style={{ color: 'var(--pink)' }}>continuous index (0–1)</strong> computed separately
            for Innings 1 (target-setting) and Innings 2 (chasing). A delivery is classified as{' '}
            <strong style={{ color: 'var(--pink)' }}>High Pressure</strong> when the index ≥ 0.65.
          </p>
          <p style={{ marginTop: 8, color: 'var(--gold)', fontWeight: 600 }}>
            Source: <code>pressure_engine.py → classify_pressure()</code>
          </p>
        </div>

        <Formula title="Innings 2 — Chase Pressure Score" description="Computed inside compute_chase_pressure_score(). The raw score is capped at 1.5 before final normalisation to [0,1].">
          <Code>{`# From pressure_engine.py → compute_chase_pressure_score()

rrr_pressure = clip((required_run_rate - 7.0) / 7.0, 0.0, 1.5)
wkt_risk     = clip((10.0 - wickets_in_hand) / 6.0,  0.0, 1.5)
time_factor  = 1.3  if balls_remaining <= 30
               1.1  if balls_remaining <= 60
               1.0  otherwise

raw_score    = (0.55 × rrr_pressure
              + 0.35 × wkt_risk
              + 0.10 × is_Death_phase) × time_factor

pressure_index (inn2) = clip(raw_score / 1.5, 0.0, 1.0)`}</Code>
        </Formula>

        <Formula title="Innings 1 — Setting Pressure Score" description="Computed inside compute_setting_pressure_score(). Takes the max of collapse_factor and death_factor, then adds sluggish CRR pressure.">
          <Code>{`# From pressure_engine.py → compute_setting_pressure_score()

# 1. Collapse pressure
early_collapse = (phase == 'Powerplay') AND (wickets_lost >= 3) → 0.85
mid_collapse   = (phase == 'Middle')    AND (wickets_lost >= 5) → 0.90
default        = (wickets_lost / 10.0) × 0.5

collapse_factor = max(early_collapse, mid_collapse, default)

# 2. Death overs urgency
death_factor    = 0.95   if phase == 'Death' AND wickets_in_hand <= 4
                  0.75   if phase == 'Death'
                  0.20   otherwise

# 3. Sluggish run-rate pressure (late overs, low scoring)
sluggish_factor = 0.30   if over > 10 AND current_run_rate < 7.0
                  0.00   otherwise

raw_score = max(collapse_factor, death_factor) + sluggish_factor
pressure_index (inn1) = clip(raw_score, 0.0, 1.0)`}</Code>
        </Formula>

        <Formula title="Pressure Tier Classification">
          <Code>{`# From pressure_engine.py → classify_pressure()

pressure_tier =
  "High"   if pressure_index >= 0.65   ← used as 'is_high_pressure'
  "Medium" if 0.35 <= index < 0.65     ← used as 'is_medium_pressure'
  "Low"    if pressure_index < 0.35

is_pressure_ball = pressure_index >= 0.50   # (broader flag, used for reference)`}</Code>
        </Formula>

        <Callout type="note">
          <strong>Distribution (all 200,999 deliveries):</strong>{' '}
          High Pressure — 48,324 (24.0%) | Medium — 20,224 (10.1%) | Low/Normal — 132,451 (65.9%).
          Of the 48,324 high-pressure deliveries, 71.4% arise from Innings 1 (Death-over acceleration and collapse scenarios)
          and 28.6% from Innings 2 (chase situations with high Required Run Rate and/or low wickets in hand).
          Innings 1 death overs broadly qualify because the pressure model rewards the attacking urgency required
          from both batting and bowling sides in the final 5 overs of a T20 innings.
        </Callout>
      </Section>

      {/* ── 3. INNINGS PHASE DEFINITIONS ── */}
      <Section title="3. Innings Phase & Match State Definitions" accent="blue">
        <Formula title="Phase Definitions (from data_cleaning.py)">
          <Code>{`# From data_cleaning.py → clean_and_engineer_ball_by_ball()

phase = "Powerplay"  if overid <= 6
        "Middle"     if 7 <= overid <= 15
        "Death"      if overid >= 16

# Legal delivery (from config.py → ILLEGAL_BALL_EXTRAS)
is_legal_ball = extras_type NOT IN {'wide', 'Overstep', 'other'}

# Batter faces the ball on all deliveries EXCEPT wides
is_ball_faced = (extras_type != 'wide')

# Bowler runs conceded (MCC Rule: byes & leg-byes charged to fielding side, NOT bowler)
bowler_runs_conceded = 0
    if extras_type IN {'byes', 'legbyes', 'Penalty'}
else batter_runs + extra_runs

# Bowler-credited wickets (from config.py → BOWLER_CREDITED_DISMISSALS)
is_bowler_wicket = is_wicket AND dismissal_type IN
    {'Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket'}
# RunOut, RetireOut, Obstructing are NOT credited to bowler`}</Code>
        </Formula>
      </Section>

      {/* ── 4. ELIGIBILITY ── */}
      <Section title="4. Minimum Eligibility Thresholds" accent="gold">
        <Callout type="caution">
          These values are taken directly from <code>config.py</code>. Apply before any ranking is computed.
        </Callout>
        <div style={{
          display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16,
        }}>
          <div style={{ background: 'rgba(255,215,0,0.06)', border: '1px solid rgba(255,215,0,0.25)', borderRadius: 12, padding: 18 }}>
            <div style={{ color: 'var(--gold)', fontWeight: 700, marginBottom: 12 }}>🏏 Batters</div>
            <Code>{`# config.py
MIN_PRESSURE_BALLS_FACED_BATTER = 60
MIN_PRESSURE_INNINGS            = 5
MIN_MATCHES_PLAYED              = 10`}</Code>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              A batter must have faced ≥ 60 balls in high-pressure situations, appeared in ≥ 5 pressure innings,
              and played ≥ 10 overall matches to qualify.
            </div>
          </div>
          <div style={{ background: 'rgba(14,165,233,0.06)', border: '1px solid rgba(14,165,233,0.25)', borderRadius: 12, padding: 18 }}>
            <div style={{ color: 'var(--blue)', fontWeight: 700, marginBottom: 12 }}>🎳 Bowlers</div>
            <Code>{`# config.py
MIN_PRESSURE_BALLS_BOWLED_BOWLER = 60
MIN_MATCHES_PLAYED               = 10`}</Code>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              A bowler must have bowled ≥ 60 legal deliveries in high-pressure situations
              and appeared in ≥ 10 overall matches to qualify.
            </div>
          </div>
        </div>
      </Section>

      {/* ── 5. BATTING METRICS ── */}
      <Section title="5. Batting Metrics Calculation" accent="pink">
        <Formula title="Core Batting Metrics (batting_metrics.py)">
          <Code>{`# From batting_metrics.py → compute_batter_aggregates()

strike_rate   = (runs / balls_faced) × 100       # balls_faced excludes wides
average       = runs / dismissals                 # or runs if dismissals == 0
boundary_pct  = (fours + sixes) / balls_faced × 100
dot_pct       = dot_balls / balls_faced × 100

# Computed for BOTH baseline (all deliveries) and pressure (is_high_pressure) subsets
# Using prefixes: norm_ and press_`}</Code>
        </Formula>

        <Formula title="Comparative Lift Metrics (batting_metrics.py → build_batting_profile())">
          <Code>{`# From batting_metrics.py → build_batting_profile()

sr_lift          = press_strike_rate - norm_strike_rate        # absolute points gained
boundary_lift    = press_boundary_pct - norm_boundary_pct      # absolute % points gained
dot_reduction    = norm_dot_pct - press_dot_pct                # absolute % points saved
                   (positive = fewer dots under pressure)`}</Code>
          <Callout type="note">
            <strong>Note:</strong> <code>sr_lift</code> is an <em>absolute difference</em> in strike-rate points,
            not a percentage change. For example, Kohli: 191.22 − 145.24 = 45.98 points.
          </Callout>
        </Formula>
      </Section>

      {/* ── 6. BATTING RELIABILITY ── */}
      <Section title="6. Batting Reliability Score" accent="pink">
        <Callout type="warning">
          The reliability score is <strong>NOT</strong> a simple weighted sum of sr_lift and boundary_lift.
          It uses a 5-component model with min-max normalisation scaled to the eligible-player distribution.
        </Callout>

        <Formula title="Step 1 — Per-Component MinMax Normalisation (reliability_model.py)">
          <Code>{`# From reliability_model.py → score_batting_reliability() → scale_col()
# Applied to each component independently across all eligible batters

p05 = component.quantile(0.05)
p95 = component.quantile(0.95)
clipped = clip(component, p05, p95)
normalised = (clipped - p05) / (p95 - p05 + 1e-6)         # 0.0 → 1.0
# For dot_pct: normalised = 1 - normalised  (lower dot % = better)`}</Code>
        </Formula>

        <Formula title="Step 2 — Composite Raw Score" description="Source: reliability_model.py → score_batting_reliability()">
          <Code>{`# From reliability_model.py — exact weights

raw_bat_score = (
    0.35 × scale(press_strike_rate)      # Pressure SR   — 35%
  + 0.20 × scale(sr_lift)                # SR Lift        — 20%
  + 0.20 × scale(press_average)          # Pressure Avg   — 20%
  + 0.15 × scale(press_boundary_pct)     # Boundary%      — 15%
  + 0.10 × scale(press_dot_pct, inv=True)# Dot% (less=better) — 10%
) × 100.0`}</Code>
        </Formula>

        <div style={{ marginBottom: 14 }}>
          <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: 10 }}>Component Weight Summary</div>
          <WeightRow metric="Pressure Strike Rate"      weight="35%"  note="Primary measure of attacking intent under pressure" />
          <WeightRow metric="Strike Rate Lift (absolute)" weight="20%"  note="Improvement vs own normal baseline" />
          <WeightRow metric="Pressure Batting Average"  weight="20%"  note="Ability to stay at the crease under pressure" />
          <WeightRow metric="Pressure Boundary %"       weight="15%"  note="Scoring-shot frequency under pressure" />
          <WeightRow metric="Pressure Dot Ball % (inverted)" weight="10%" note="Lower dot% = better score" />
        </div>

        <Formula title="Step 3 — Confidence Factor & Final Score">
          <Code>{`# From reliability_model.py → compute_sample_confidence()
# Target = 250 pressure balls faced; min = MIN_PRESSURE_BALLS_FACED_BATTER = 60

factor           = clip((press_balls_faced - 60) / (250 - 60), 0.0, 1.0)
confidence_factor = 0.60 + 0.40 × sqrt(factor)
# Range: 0.60 (minimum, at 60 balls) → 1.00 (at 250+ balls)

# Final reliability score (Bayesian shrinkage towards 50 for small samples)
reliability_score = raw_bat_score × confidence_factor
                  + 50.0 × (1.0 - confidence_factor)
reliability_score = round(reliability_score, 2)`}</Code>
        </Formula>

        <Callout type="note">
          <strong>Virat Kohli confidence note:</strong> Kohli has only 148 pressure balls faced (confidence_factor = 0.872),
          slightly below the full-confidence threshold of 250. His exceptional normalised score across all 5 components
          (particularly press_SR of 191.22 and press_avg of 47.17) is strong enough to rank #1 even after the 12.8%
          Bayesian discount. With only 13 pressure innings across 92 overall matches, it is possible that Kohli was
          tactically shielded from the most extreme pressure situations, which may mean his pressure sample is from
          moderate rather than extreme pressure moments.
        </Callout>
      </Section>

      {/* ── 7. BOWLING METRICS ── */}
      <Section title="7. Bowling Metrics Calculation" accent="blue">
        <Formula title="Core Bowling Metrics (bowling_metrics.py)">
          <Code>{`# From bowling_metrics.py → compute_bowler_aggregates()

overs        = legal_balls / 6.0
economy      = runs_conceded / overs               # runs per over (RPO)
strike_rate  = legal_balls / wickets               # balls per wicket
average      = runs_conceded / wickets
dot_pct      = dot_balls / total_balls × 100       # total_balls includes extras
boundary_conceded_pct = (fours + sixes) / total_balls × 100

# Computed for BOTH baseline (all deliveries) and pressure (is_high_pressure)
# Using prefixes: norm_ and press_`}</Code>
        </Formula>

        <Formula title="Comparative Suppression Metrics (bowling_metrics.py → build_bowling_profile())">
          <Code>{`# From bowling_metrics.py

econ_suppression    = norm_economy - press_economy
                      (positive = fewer RPO conceded under pressure)
dot_lift            = press_dot_pct - norm_dot_pct
                      (positive = more dot balls under pressure)
boundary_prevention = norm_boundary_conceded_pct - press_boundary_conceded_pct
                      (positive = fewer boundaries under pressure)
wkt_rate_lift       = (press_wickets / press_legal_balls
                      - norm_wickets / norm_legal_balls) × 100
                      (wicket rate change per ball under pressure)`}</Code>
        </Formula>
      </Section>

      {/* ── 8. BOWLING RELIABILITY ── */}
      <Section title="8. Bowling Reliability Score" accent="blue">
        <Formula title="Step 1 — MinMax Normalisation (same scale_col as batting)">
          <Code>{`# From reliability_model.py → score_bowling_reliability() → scale_col()
# press_economy and press_strike_rate use higher_is_better=False (inverted)
# press_dot_pct and econ_suppression use higher_is_better=True`}</Code>
        </Formula>

        <Formula title="Step 2 — Composite Raw Score" description="Source: reliability_model.py → score_bowling_reliability()">
          <Code>{`# From reliability_model.py — exact weights

raw_bowl_score = (
    0.30 × scale(press_economy,                inv=True)  # Press Economy  — 30%
  + 0.25 × scale(press_strike_rate,            inv=True)  # Press Bow-SR   — 25%
  + 0.20 × scale(econ_suppression,             inv=False) # Econ Suppress  — 20%
  + 0.15 × scale(press_dot_pct,                inv=False) # Press Dot%     — 15%
  + 0.10 × scale(press_boundary_conceded_pct,  inv=True)  # Boundary Prev  — 10%
) × 100.0`}</Code>
        </Formula>

        <div style={{ marginBottom: 14 }}>
          <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: 10 }}>Component Weight Summary</div>
          <WeightRow metric="Pressure Economy Rate (RPO)"           weight="30%"  note="Primary measure — lower is better" />
          <WeightRow metric="Pressure Bowling Strike Rate (inverted)" weight="25%" note="Wicket-taking frequency under pressure" />
          <WeightRow metric="Economy Suppression (norm − press)"    weight="20%"  note="RPO improvement vs own normal baseline" />
          <WeightRow metric="Pressure Dot Ball %"                    weight="15%"  note="Ability to stifle scoring" />
          <WeightRow metric="Pressure Boundary Conceded % (inverted)" weight="10%" note="Boundary prevention under pressure" />
        </div>

        <Formula title="Step 3 — Confidence Factor & Final Score">
          <Code>{`# From reliability_model.py → compute_sample_confidence()
# Target = 250 pressure legal balls; min = MIN_PRESSURE_BALLS_BOWLED_BOWLER = 60

factor            = clip((press_legal_balls - 60) / (250 - 60), 0.0, 1.0)
confidence_factor = 0.60 + 0.40 × sqrt(factor)

reliability_score = raw_bowl_score × confidence_factor
                  + 50.0 × (1.0 - confidence_factor)
reliability_score = round(reliability_score, 2)`}</Code>
        </Formula>
      </Section>

      {/* ── 9. ANOMALIES & CAVEATS ── */}
      <Section title="9. Anomalies, Caveats & Limitations" accent="gold">

        <CollapseSection title="⚠️ Sufiyan Muqeem (Bowler Rank 10) — Negative Economy Suppression">
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.75 }}>
            <p>Sufiyan Muqeem's pressure economy (6.44 RPO) is <strong>higher</strong> than his normal economy (6.00 RPO),
            yielding a negative econ_suppression of −0.44. This means he concedes <em>more</em> runs per over under pressure
            on average.</p>
            <p style={{ marginTop: 8 }}>He ranks 10th because the bowling reliability model rewards <strong>multiple dimensions</strong> of pressure performance:</p>
            <ul style={{ marginTop: 8, marginLeft: 20, display: 'flex', flexDirection: 'column', gap: 4 }}>
              <li>His <strong>pressure dot-ball lift of +6.47%</strong> (highest in the top 10) earns a strong normalised score on that component (15% weight)</li>
              <li>His <strong>pressure bowling strike rate is competitive</strong> (12 wickets in 122 balls = 10.17 balls/wkt under pressure)</li>
              <li>His <strong>boundary prevention is positive</strong></li>
            </ul>
            <p style={{ marginTop: 8 }}>The model correctly captures that he suppresses boundary-scoring and induces dots under pressure (reducing hitting opportunities) even though the total RPO is marginally higher. Users interpreting economy in isolation should note this nuance.</p>
          </div>
        </CollapseSection>

        <CollapseSection title="ℹ️ Innings 1 Dominance — 71.4% of High-Pressure Deliveries">
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.75 }}>
            <p>71.4% of the 48,324 high-pressure deliveries arise from Innings 1 scenarios — primarily Death overs (overs 16–20)
            where the pressure model assigns high scores due to batting urgency and limited wickets-in-hand.
            Only 28.6% come from Innings 2 chase scenarios.</p>
            <p style={{ marginTop: 8 }}>This is a property of the continuous model: Death-over batting is genuinely high-pressure
            for <em>both</em> sides (the batting team must accelerate; the bowling team must protect).
            Players who perform well in both Innings 1 death overs and tight Innings 2 chases are captured robustly.</p>
            <p style={{ marginTop: 8 }}>Evaluators preferring a chase-only or pure-binary pressure definition may weight
            Innings 2 performance differently. This is acknowledged as a methodological choice.</p>
          </div>
        </CollapseSection>

        <CollapseSection title="ℹ️ Virat Kohli — Low Pressure-Ball Sample (148 balls, 13 innings)">
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.75 }}>
            <p>Kohli has 148 pressure balls faced across 92 overall matches — roughly 1.6 pressure balls per match.
            This is notably lower than players like Rinku Singh (640) or Tristan Stubbs (457).</p>
            <p style={{ marginTop: 8 }}>Possible explanations: (a) As a top-order batter who often bats in Powerplay
            (which rarely qualifies as high-pressure in the first innings model), his pressure exposure is naturally lower.
            (b) In successful teams, top-order batters may bat out of pressure situations before they escalate.
            (c) His confidence_factor = 0.872 (not 1.0), so his score already carries a Bayesian discount.</p>
            <p style={{ marginTop: 8 }}>His high ranking reflects extremely high quality in the pressure situations
            he <em>did</em> face — 191.22 press SR, 47.17 press avg — which survives the confidence discount.</p>
          </div>
        </CollapseSection>

        <CollapseSection title="⚠️ General Limitations">
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.75 }}>
            <ul style={{ marginLeft: 20, display: 'flex', flexDirection: 'column', gap: 8 }}>
              <li>No T20 World Cup data (2022, 2024 events absent). Rankings do not capture ICC tournament pressure performances.</li>
              <li>Venue, pitch conditions, day/night factors and opposition quality are not modelled.</li>
              <li>Sample size varies significantly. Confidence weighting partially adjusts for this but cannot fully compensate for rare-exposure players.</li>
              <li>Historical team associations (Layer 2) are based on <code>playing_eleven.csv</code> appearances in the supplied dataset only. They do not confirm current squad membership or IPL 2027 auction availability.</li>
              <li>Overseas player rules, BCCI retentions and Right-to-Match (RTM) availability must be verified independently before auction targeting.</li>
            </ul>
          </div>
        </CollapseSection>
      </Section>

      {/* ── 10. REPRODUCIBILITY ── */}
      <Section title="10. Reproducibility" accent="green">
        <div style={{ background: 'rgba(34,197,94,0.06)', border: '1px solid rgba(34,197,94,0.25)', borderRadius: 12, padding: 20, fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.75 }}>
          <p>The entire pipeline is reproducible from the six supplied raw CSV files:</p>
          <Code>{`1. python src/data_cleaning.py         → data/processed/ball_by_ball_processed.parquet
2. python src/pressure_engine.py       → data/processed/ball_by_ball_pressure_classified.parquet
3. python src/batting_metrics.py       → (batting profiles in memory)
4. python src/bowling_metrics.py       → (bowling profiles in memory)
5. python src/reliability_model.py     → data/outputs/all_eligible_*.csv
6. python src/ranking_engine.py        → data/outputs/top_10_*.csv
7. python src/generate_rr_recruitment_layer.py → rr_recruitment_*.csv/.parquet`}</Code>
          <p style={{ marginTop: 8 }}>
            All intermediate and final output files are deterministic given the same raw CSVs.
            Rankings have been independently recalculated and verified against stored output — all 20 player entries match exactly.
          </p>
        </div>
      </Section>
    </div>
  )
}
