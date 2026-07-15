import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Rocket, Lock, User, Key, ChevronRight } from 'lucide-react';

export const Login: React.FC = () => {
  const [studentId, setStudentId] = useState('11391');
  const [password, setPassword] = useState('password');
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('pla_student_id', studentId);
    localStorage.setItem('pla_student_name', 'Student ' + studentId);
    localStorage.setItem('pla_onboarding_completed', 'true');
    navigate('/');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-space-dark)' }}>
      {/* Background glow effects */}
      <div style={{ position: 'absolute', width: '600px', height: '600px', background: 'radial-gradient(circle, rgba(0,243,255,0.05) 0%, transparent 70%)', top: '10%', left: '20%' }} />
      <div style={{ position: 'absolute', width: '500px', height: '500px', background: 'radial-gradient(circle, rgba(157,0,255,0.05) 0%, transparent 70%)', bottom: '10%', right: '20%' }} />

      <div className="glass-panel animate-fade-in" style={{ padding: '48px', width: '100%', maxWidth: '460px', position: 'relative', zIndex: 10 }}>
        
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '40px' }}>
          <div style={{ width: 80, height: 80, borderRadius: '50%', background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid var(--neon-cyan)', boxShadow: 'var(--shadow-glow-cyan)', marginBottom: '24px' }}>
            <Rocket size={40} color="var(--neon-cyan)" />
          </div>
          <h1 style={{ color: 'var(--text-primary)', margin: 0, fontSize: '1.8rem', letterSpacing: '0.1em' }}>MISSION CONTROL</h1>
          <div style={{ color: 'var(--neon-purple)', fontWeight: 600, letterSpacing: '0.2em', fontSize: '0.8rem', marginTop: '8px' }}>AUTHORIZED PERSONNEL ONLY</div>
        </div>

        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <User size={14} /> Agent ID
            </label>
            <div style={{ position: 'relative' }}>
              <input 
                type="text" 
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                style={{ width: '100%', padding: '12px 16px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', borderRadius: '6px', color: 'white', outline: 'none', fontSize: '1rem', transition: 'border 0.3s' }} 
                onFocus={(e) => e.target.style.borderColor = 'var(--neon-cyan)'}
                onBlur={(e) => e.target.style.borderColor = 'var(--glass-border)'}
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <Key size={14} /> Passcode
            </label>
            <div style={{ position: 'relative' }}>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ width: '100%', padding: '12px 16px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', borderRadius: '6px', color: 'white', outline: 'none', fontSize: '1rem', transition: 'border 0.3s' }} 
                onFocus={(e) => e.target.style.borderColor = 'var(--neon-cyan)'}
                onBlur={(e) => e.target.style.borderColor = 'var(--glass-border)'}
              />
            </div>
          </div>

          <button type="submit" className="btn-mission" style={{ marginTop: '16px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', fontSize: '1rem' }}>
            <Lock size={18} /> INITIATE LOGIN SEQUENCE <ChevronRight size={18} />
          </button>

          <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.85rem' }}>
            <span style={{ color: 'var(--text-secondary)' }}>New recruit? </span>
            <Link to="/signup" style={{ color: 'var(--neon-purple)', textDecoration: 'none', fontWeight: 600 }}>Signup here.</Link>
          </div>

        </form>

      </div>
    </div>
  );
};
