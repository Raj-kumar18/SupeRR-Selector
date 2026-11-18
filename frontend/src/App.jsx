import { BrowserRouter, Routes, Route, NavLink, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import {
  LayoutDashboard, TrendingUp, Zap, Activity,
  Users, Shield, Calculator, ChevronLeft, ChevronRight, Menu
} from 'lucide-react'
import ExecutiveDashboard from './pages/ExecutiveDashboard'
import BattersIntelligence from './pages/BattersIntelligence'
import BowlersIntelligence from './pages/BowlersIntelligence'
import RecruitmentMatrix from './pages/RecruitmentMatrix'
import PlayerComparison from './pages/PlayerComparison'
import MathEngine from './pages/MathEngine'
import './index.css'

const NAV = [
  { to: '/',            icon: LayoutDashboard, label: 'Executive Dashboard' },
  { to: '/batters',     icon: TrendingUp,       label: 'Batters Intelligence' },
  { to: '/bowlers',     icon: Zap,              label: 'Bowlers Intelligence' },
  { to: '/recruitment', icon: Users,            label: 'RR Recruitment Matrix' },
  { to: '/compare',     icon: Activity,         label: 'Player Comparison' },
  { to: '/math',        icon: Calculator,       label: 'Mathematical Engine' },
]

function RRLogo() {
  return (
    <svg viewBox="0 0 60 60" width="42" height="42" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="rrg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#EA1A7F"/>
          <stop offset="100%" stopColor="#0EA5E9"/>
        </linearGradient>
      </defs>
      <circle cx="30" cy="30" r="28" fill="url(#rrg)" opacity="0.15" stroke="url(#rrg)" strokeWidth="1.5"/>
      <text x="50%" y="38" textAnchor="middle" fontFamily="Rajdhani,Inter,sans-serif" fontWeight="700" fontSize="22" fill="url(#rrg)">RR</text>
    </svg>
  )
}

function Sidebar({ collapsed, setCollapsed }) {
  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      {/* Brand */}
      <div style={{ padding: '20px 16px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 12, minHeight: 72 }}>
        <RRLogo />
        {!collapsed && (
          <div>
            <div style={{ fontFamily: 'Rajdhani,sans-serif', fontWeight: 700, fontSize: '1.1rem', color: '#fff', lineHeight: 1.1 }}>SupeRR Selector</div>
            <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>RR IPL 2027 War Room</div>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: '16px 8px' }}>
        {NAV.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              padding: '10px 12px',
              borderRadius: 10,
              marginBottom: 4,
              textDecoration: 'none',
              color: isActive ? '#fff' : 'var(--text-muted)',
              background: isActive ? 'linear-gradient(135deg,rgba(234,26,127,0.2),rgba(14,165,233,0.1))' : 'transparent',
              borderLeft: isActive ? '3px solid var(--pink)' : '3px solid transparent',
              transition: 'all 0.2s',
              fontSize: '0.875rem',
              fontWeight: isActive ? 600 : 400,
              whiteSpace: 'nowrap',
              overflow: 'hidden',
            })}
          >
            <Icon size={18} style={{ minWidth: 18 }} />
            {!collapsed && label}
          </NavLink>
        ))}
      </nav>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        style={{
          margin: '12px', padding: '10px', border: '1px solid var(--border)',
          borderRadius: 10, background: 'transparent', color: 'var(--text-muted)',
          cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
          transition: 'all 0.2s',
        }}
        onMouseEnter={e => { e.target.style.borderColor = 'var(--pink)'; e.target.style.color = 'var(--pink)' }}
        onMouseLeave={e => { e.target.style.borderColor = 'var(--border)'; e.target.style.color = 'var(--text-muted)' }}
      >
        {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      {/* Footer */}
      {!collapsed && (
        <div style={{ padding: '12px 16px', borderTop: '1px solid var(--border)', fontSize: '0.65rem', color: 'var(--text-muted)', textAlign: 'center' }}>
          Powered by Ball-by-Ball Analytics<br/>
          <span style={{ color: 'var(--pink)', fontWeight: 600 }}>© Rajasthan Royals 2026</span>
        </div>
      )}
    </aside>
  )
}

function TopBar({ collapsed, setCollapsed }) {
  return (
    <div className="topbar">
      <button onClick={() => setCollapsed(!collapsed)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
        <Menu size={20} />
      </button>
      <div style={{ flex: 1 }} />
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <div style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--green)', boxShadow: '0 0 8px var(--green)' }} />
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Live Analytics Engine</span>
      </div>
      <div style={{
        background: 'linear-gradient(135deg,rgba(234,26,127,0.15),rgba(14,165,233,0.1))',
        border: '1px solid rgba(234,26,127,0.3)',
        borderRadius: 8, padding: '4px 12px',
        fontSize: '0.72rem', fontWeight: 600, color: 'var(--pink)',
        letterSpacing: '0.05em', textTransform: 'uppercase'
      }}>
        IPL 2027 Auction Season
      </div>
    </div>
  )
}

export default function App() {
  const [collapsed, setCollapsed] = useState(false)
  return (
    <BrowserRouter>
      <div className="layout">
        <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />
        <div className="main-content">
          <TopBar collapsed={collapsed} setCollapsed={setCollapsed} />
          <div className="page-content">
            <Routes>
              <Route path="/"            element={<ExecutiveDashboard />} />
              <Route path="/batters"     element={<BattersIntelligence />} />
              <Route path="/bowlers"     element={<BowlersIntelligence />} />
              <Route path="/recruitment" element={<RecruitmentMatrix />} />
              <Route path="/compare"     element={<PlayerComparison />} />
              <Route path="/math"        element={<MathEngine />} />
            </Routes>
          </div>
        </div>
      </div>
    </BrowserRouter>
  )
}
