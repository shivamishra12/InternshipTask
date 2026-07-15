import React, { useState, useEffect } from 'react';
import { Map, Cpu, Calendar, Clock, CheckCircle, Circle, ArrowRight } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export const MissionPlanner: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = '11391';

  useEffect(() => {
    const fetchPlanner = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/study-plan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_id: parseInt(studentId) })
        });
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchPlanner();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--neon-blue)" />
      <div style={{ color: 'var(--neon-blue)', letterSpacing: '0.1em' }}>GENERATING MISSION WAYPOINTS...</div>
    </div>
  );

  const planMarkdown = data?.markdown_plan || '';
  
  // Custom renderer for markdown to style it like NASA UI
  const components = {
    h1: ({node, ...props}:any) => <h2 style={{ color: 'var(--neon-blue)', marginBottom: '16px', borderBottom: '1px solid var(--glass-border)', paddingBottom: '8px' }} {...props} />,
    h2: ({node, ...props}:any) => <h3 style={{ color: 'var(--text-primary)', marginTop: '24px', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }} {...props}><Calendar size={18} color="var(--neon-blue)"/> {props.children}</h3>,
    p: ({node, ...props}:any) => <p style={{ color: 'var(--text-secondary)', marginBottom: '12px' }} {...props} />,
    ul: ({node, ...props}:any) => <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }} {...props} />,
    li: ({node, ...props}:any) => (
      <div className="glass-panel" style={{ padding: '16px', display: 'flex', alignItems: 'center', gap: '16px', background: 'rgba(0,102,255,0.05)' }}>
        <Circle size={20} color="var(--text-muted)" />
        <div style={{ flex: 1, color: 'var(--text-primary)' }} {...props} />
        <button className="btn-mission" style={{ padding: '4px 8px', fontSize: '0.7rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
          START <ArrowRight size={12} />
        </button>
      </div>
    ),
    strong: ({node, ...props}:any) => <span style={{ color: 'var(--neon-cyan)', fontWeight: 600 }} {...props} />
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '900px', margin: '0 auto', width: '100%' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
        <Map size={28} color="var(--neon-blue)" />
        <h2 style={{ color: 'var(--neon-blue)', margin: 0 }}>MISSION PLANNER</h2>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <Calendar size={32} color="var(--neon-blue)" />
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Mission Duration</div>
            <div className="metric-value-huge" style={{ fontSize: '1.5rem', marginTop: '4px' }}>7 DAYS</div>
          </div>
        </div>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <Clock size={32} color="var(--neon-cyan)" />
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Total Est. Time</div>
            <div className="metric-value-huge" style={{ fontSize: '1.5rem', marginTop: '4px', color: 'var(--neon-cyan)' }}>14.5 HRS</div>
          </div>
        </div>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <CheckCircle size={32} color="var(--status-ok)" />
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Completion Status</div>
            <div className="metric-value-huge" style={{ fontSize: '1.5rem', marginTop: '4px', color: 'var(--status-ok)' }}>0%</div>
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '32px', marginTop: '12px' }}>
        <ReactMarkdown components={components as any}>
          {planMarkdown || '*No plan data found from backend.*'}
        </ReactMarkdown>
      </div>
    </div>
  );
};
