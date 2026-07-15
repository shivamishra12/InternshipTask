import React, { useState, useEffect } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { 
  Rocket, Activity, ShieldAlert, ScanSearch, Target, BookOpen, 
  Map, BarChart2, User, Settings, LogOut, Bell, Search, Bot,
  Database, Server, Cpu
} from 'lucide-react';

const navItems = [
  { path: '/', icon: <Rocket size={20} />, label: 'Mission Control' },
  { path: '/performance', icon: <Activity size={20} />, label: 'Performance Engine' },
  { path: '/risk', icon: <ShieldAlert size={20} />, label: 'Risk Radar' },
  { path: '/knowledge', icon: <ScanSearch size={20} />, label: 'Knowledge Scanner' },
  { path: '/weak-topics', icon: <Target size={20} />, label: 'Weak Topic Analyzer' },
  { path: '/resources', icon: <BookOpen size={20} />, label: 'Learning Resources' },
  { path: '/planner', icon: <Map size={20} />, label: 'Mission Planner' },
  { path: '/analytics', icon: <BarChart2 size={20} />, label: 'Analytics Center' },
  { path: '/profile', icon: <User size={20} />, label: 'Student Profile' },
  { path: '/settings', icon: <Settings size={20} />, label: 'Settings' },
];

export const Layout: React.FC = () => {
  const [time, setTime] = useState(new Date().toLocaleTimeString('en-US', { hour12: false }));
  
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString('en-US', { hour12: false })), 1000);
    return () => clearInterval(timer);
  }, []);

  const navigate = useNavigate();
  useEffect(() => {
    if (localStorage.getItem('pla_onboarding_completed') !== 'true' && localStorage.getItem('pla_student_id') !== '11391') {
      navigate('/login');
    }
  }, [navigate]);

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar-container">
        <div style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '12px', borderBottom: '1px solid var(--glass-border)' }}>
          <Rocket color="var(--neon-cyan)" size={28} />
          <div>
            <h2 style={{ fontSize: '1.1rem', margin: 0, color: 'var(--text-primary)' }}>PLA</h2>
            <h4 style={{ margin: 0, fontSize: '0.7rem' }}>Mission Control</h4>
          </div>
        </div>
        
        <nav style={{ flex: 1, padding: '16px 0', overflowY: 'auto' }}>
          {navItems.map((item) => (
            <NavLink 
              key={item.path} 
              to={item.path} 
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              {item.icon}
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        
        <div style={{ padding: '16px 0', borderTop: '1px solid var(--glass-border)' }}>
          <button 
            className="nav-item" 
            onClick={() => {
              localStorage.clear();
              navigate('/login');
            }}
            style={{ width: '100%', background: 'none', border: 'none', cursor: 'pointer', textAlign: 'left' }}>
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Area */}
      <div className="main-wrapper">
        {/* Header */}
        <header className="global-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <User size={18} color="var(--text-secondary)" />
              <span style={{ fontWeight: 500 }}>Student: <span style={{ color: 'var(--neon-cyan)' }}>{localStorage.getItem('pla_student_name') || '11391'}</span></span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Target size={18} color="var(--text-secondary)" />
              <span style={{ fontWeight: 500 }}>Mission: <span style={{ color: 'var(--neon-purple)' }}>{localStorage.getItem('pla_student_course') || 'AAA'} Module Prep</span></span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--neon-blue)', fontFamily: 'monospace', fontSize: '1.1rem' }}>
              {time} T-MINUS
            </div>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', padding: '4px 12px', gap: '8px', borderRadius: '20px' }}>
              <Search size={16} color="var(--text-secondary)" />
              <input type="text" placeholder="Search parameters..." style={{ background: 'transparent', border: 'none', color: 'white', width: '150px', outline: 'none', fontSize: '0.85rem' }} />
            </div>
            
            <button style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', position: 'relative' }}>
              <Bell size={20} />
              <span style={{ position: 'absolute', top: -2, right: -2, width: 8, height: 8, background: 'var(--status-critical)', borderRadius: '50%', boxShadow: '0 0 5px var(--status-critical)' }}></span>
            </button>
            
            <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'var(--glass-border)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid var(--neon-cyan)' }}>
              <span style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>
                {(localStorage.getItem('pla_student_name') || 'OP').substring(0,2).toUpperCase()}
              </span>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="content-scroll">
          <Outlet />
        </main>

        {/* Footer */}
        <footer className="global-footer">
          <div style={{ display: 'flex', gap: '16px' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Server size={14} /> Backend: <span className="status-dot ok"></span>
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Database size={14} /> Database: <span className="status-dot ok"></span>
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Cpu size={14} /> Models: <span className="status-dot ok"></span>
            </span>
          </div>
          <div>
            PLA OS v1.0.0 &copy; 2026 SpaceEd Corp.
          </div>
        </footer>
      </div>

      {/* Floating AI Assistant */}
      <div className="fab-ai" title="AI Mission Assistant">
        <Bot size={24} color="var(--neon-purple)" />
      </div>
    </div>
  );
};
