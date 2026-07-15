import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Rocket, UserPlus, User, Key, Mail, BookOpen, ChevronRight } from 'lucide-react';

export const Signup: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [course, setCourse] = useState('AAA');
  const navigate = useNavigate();

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    
    // Save to local storage before redirecting to assessment
    localStorage.setItem('pla_student_name', name);
    localStorage.setItem('pla_student_course', course);
    localStorage.setItem('pla_onboarding_completed', 'false');
    
    navigate('/assessment');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-space-dark)' }}>
      {/* Background glow effects */}
      <div style={{ position: 'absolute', width: '600px', height: '600px', background: 'radial-gradient(circle, rgba(157,0,255,0.05) 0%, transparent 70%)', top: '10%', right: '20%' }} />
      <div style={{ position: 'absolute', width: '500px', height: '500px', background: 'radial-gradient(circle, rgba(0,243,255,0.05) 0%, transparent 70%)', bottom: '10%', left: '20%' }} />

      <div className="glass-panel animate-fade-in" style={{ padding: '48px', width: '100%', maxWidth: '500px', position: 'relative', zIndex: 10 }}>
        
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '32px' }}>
          <div style={{ width: 80, height: 80, borderRadius: '50%', background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid var(--neon-purple)', boxShadow: 'var(--shadow-glow-purple)', marginBottom: '24px' }}>
            <UserPlus size={40} color="var(--neon-purple)" />
          </div>
          <h1 style={{ color: 'var(--text-primary)', margin: 0, fontSize: '1.8rem', letterSpacing: '0.1em' }}>CADET REGISTRATION</h1>
          <div style={{ color: 'var(--neon-cyan)', fontWeight: 600, letterSpacing: '0.2em', fontSize: '0.8rem', marginTop: '8px' }}>NEW MISSION PROFILE</div>
        </div>

        <form onSubmit={handleSignup} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <User size={14} /> Full Name
            </label>
            <input 
              type="text" 
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Alex Mercer"
              style={{ width: '100%', padding: '12px 16px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', borderRadius: '6px', color: 'white', outline: 'none', fontSize: '1rem', transition: 'border 0.3s' }} 
              onFocus={(e) => e.target.style.borderColor = 'var(--neon-purple)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--glass-border)'}
            />
          </div>

          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <Mail size={14} /> Comm Link (Email)
            </label>
            <input 
              type="email" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="alex@space-ed.com"
              style={{ width: '100%', padding: '12px 16px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', borderRadius: '6px', color: 'white', outline: 'none', fontSize: '1rem', transition: 'border 0.3s' }} 
              onFocus={(e) => e.target.style.borderColor = 'var(--neon-purple)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--glass-border)'}
            />
          </div>

          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <Key size={14} /> Passcode
            </label>
            <input 
              type="password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ width: '100%', padding: '12px 16px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', borderRadius: '6px', color: 'white', outline: 'none', fontSize: '1rem', transition: 'border 0.3s' }} 
              onFocus={(e) => e.target.style.borderColor = 'var(--neon-purple)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--glass-border)'}
            />
          </div>

          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <BookOpen size={14} /> Target Course Module
            </label>
            <select 
              value={course}
              onChange={(e) => setCourse(e.target.value)}
              style={{ width: '100%', padding: '12px 16px', background: 'rgba(0,0,0,0.8)', border: '1px solid var(--glass-border)', borderRadius: '6px', color: 'white', outline: 'none', fontSize: '1rem', transition: 'border 0.3s', cursor: 'pointer' }}
            >
              <option value="AAA">Module AAA - Deep Space Analytics</option>
              <option value="BBB">Module BBB - Orbital Mechanics</option>
              <option value="CCC">Module CCC - Cognitive Theory</option>
            </select>
          </div>

          <button type="submit" className="btn-mission" style={{ marginTop: '16px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', fontSize: '1rem', borderColor: 'var(--neon-purple)', color: 'var(--neon-purple)' }}>
            PROCEED TO ASSESSMENT <ChevronRight size={18} />
          </button>
          
          <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.85rem' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Already authorized? </span>
            <Link to="/login" style={{ color: 'var(--neon-cyan)', textDecoration: 'none', fontWeight: 600 }}>Login here.</Link>
          </div>

        </form>

      </div>
    </div>
  );
};
