import React, { useState, useEffect } from 'react';
import { User, Award, Shield, Star, Clock, Target, Rocket, Cpu } from 'lucide-react';

export const StudentProfile: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = '11391';

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/dashboard/${studentId}`);
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--neon-purple)" />
      <div style={{ color: 'var(--neon-purple)', letterSpacing: '0.1em' }}>LOADING AGENT PROFILE...</div>
    </div>
  );

  const student = data?.student || {};

  const badges = [
    { name: 'First Mission', icon: <Rocket size={24} color="var(--neon-cyan)"/>, date: '2026-01-15' },
    { name: 'Flawless Week', icon: <Star size={24} color="var(--status-warn)"/>, date: '2026-03-22' },
    { name: 'Risk Mitigator', icon: <Shield size={24} color="var(--neon-purple)"/>, date: '2026-05-10' },
    { name: 'Top 10%', icon: <Award size={24} color="var(--status-ok)"/>, date: '2026-06-01' }
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <User size={28} color="var(--text-primary)" />
        <h2 style={{ color: 'var(--text-primary)', margin: 0 }}>AGENT PROFILE</h2>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: '1fr 2fr' }}>
        
        {/* Left: ID Card */}
        <div className="glass-panel" style={{ padding: '32px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
          <div style={{ width: 120, height: 120, borderRadius: '50%', background: 'linear-gradient(135deg, rgba(0,243,255,0.2), rgba(157,0,255,0.2))', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '2px solid var(--neon-cyan)', marginBottom: '24px', boxShadow: 'var(--shadow-glow-cyan)' }}>
            <User size={64} color="var(--neon-cyan)" />
          </div>
          
          <h3 style={{ fontSize: '1.5rem', marginBottom: '8px', color: 'var(--text-primary)' }}>Student #{studentId}</h3>
          <div style={{ color: 'var(--neon-purple)', fontWeight: 'bold', letterSpacing: '0.1em', marginBottom: '24px' }}>CADET STATUS</div>

          <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--glass-border)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Assigned Course</span>
              <span style={{ color: 'var(--text-primary)' }}>{student.current_course || 'AAA'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--glass-border)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Registered Credits</span>
              <span style={{ color: 'var(--text-primary)' }}>{student.credits_registered || 120}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--glass-border)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>T-Minus</span>
              <span style={{ color: 'var(--neon-cyan)' }}>{student.target_exam_days_away || 14} Days</span>
            </div>
          </div>
        </div>

        {/* Right: Stats & Badges */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="dash-grid" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
            <div className="glass-panel" style={{ padding: '24px' }}>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Total Study Hours</div>
              <div className="metric-value-huge" style={{ marginTop: '8px', fontSize: '2rem' }}>248<span style={{fontSize:'1rem'}}>h</span></div>
            </div>
            <div className="glass-panel" style={{ padding: '24px' }}>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Missions Completed</div>
              <div className="metric-value-huge" style={{ marginTop: '8px', fontSize: '2rem', color: 'var(--neon-purple)' }}>42</div>
            </div>
            <div className="glass-panel" style={{ padding: '24px' }}>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Overall Rank</div>
              <div className="metric-value-huge" style={{ marginTop: '8px', fontSize: '2rem', color: 'var(--status-warn)' }}>#312</div>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
            <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Award size={20} color="var(--status-warn)"/> Mission Commendations (Badges)
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              {badges.map((badge, idx) => (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <div style={{ width: 48, height: 48, borderRadius: '50%', background: 'rgba(0,0,0,0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {badge.icon}
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{badge.name}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>Achieved: {badge.date}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
