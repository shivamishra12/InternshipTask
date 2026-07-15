import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, Target, Zap, Clock, Star, AlertTriangle, Cpu } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, AreaChart, Area, CartesianGrid } from 'recharts';

export const Dashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const studentId = '11391'; // Hardcoded for demo

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/dashboard/${studentId}`);
        if (!response.ok) throw new Error('API Error');
        const result = await response.json();
        setData(result);
      } catch (err: any) {
        setError(err.message || 'Failed to connect to backend.');
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--neon-cyan)" />
      <div style={{ color: 'var(--neon-cyan)', letterSpacing: '0.1em' }}>INITIALIZING MISSION CONTROL...</div>
    </div>
  );

  if (error) return (
    <div className="glass-panel" style={{ padding: '24px', borderColor: 'var(--status-critical)', color: 'var(--status-critical)' }}>
      <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--status-critical)' }}>
        <ShieldAlert /> CRITICAL SYSTEM FAILURE
      </h2>
      <p style={{ marginTop: '12px' }}>{error}</p>
      <button className="btn-mission" style={{ marginTop: '16px', borderColor: 'var(--status-critical)', color: 'var(--status-critical)' }} onClick={() => window.location.reload()}>
        REBOOT SYSTEM
      </button>
    </div>
  );

  const student = data?.student || {};
  const performance = data?.performance || {};
  const risk = data?.risk || {};
  
  // Mock trend data for charts since backend only gives a single value
  const mockTrend = [
    { name: 'T-5', score: 65 }, { name: 'T-4', score: 68 }, { name: 'T-3', score: 72 }, 
    { name: 'T-2', score: 75 }, { name: 'T-1', score: 73 }, { name: 'T-0', score: Math.round(performance.success_probability * 100) }
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Top Section */}
      <section className="dash-grid dash-grid-top">
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h4>Mission Status</h4>
          <div className="metric-value-huge" style={{ marginTop: '12px' }}>ACTIVE</div>
          <div style={{ color: 'var(--status-ok)', fontSize: '0.85rem', marginTop: '8px' }}>Course: {student.current_course}</div>
        </div>
        
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h4>Performance Prediction</h4>
          <div className="metric-value-huge" style={{ marginTop: '12px', color: 'var(--neon-cyan)' }}>
            {Math.round(performance.success_probability * 100)}<span style={{fontSize:'1.5rem'}}>%</span>
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '8px' }}>
            Expected: <span style={{ color: 'var(--text-primary)' }}>{performance.predicted_performance}</span>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderColor: risk.is_at_risk ? 'var(--status-critical)' : 'var(--glass-border)' }}>
          <h4>Risk Level</h4>
          <div className="metric-value-huge" style={{ marginTop: '12px', color: risk.is_at_risk ? 'var(--status-critical)' : 'var(--status-ok)' }}>
            {Math.round(risk.risk_score * 100)}<span style={{fontSize:'1.5rem'}}>%</span>
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '8px' }}>
            {risk.is_at_risk ? 'Intervention Required' : 'Nominal'}
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <h4>Knowledge Score</h4>
          <div className="metric-value-huge" style={{ marginTop: '12px', color: 'var(--neon-purple)' }}>
            84<span style={{fontSize:'1.5rem'}}>%</span>
          </div>
          <div style={{ color: 'var(--status-ok)', fontSize: '0.85rem', marginTop: '8px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Activity size={14}/> +2.4% from last week
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <h4>Time to Exam</h4>
          <div className="metric-value-huge" style={{ marginTop: '12px' }}>
            T-{student.target_exam_days_away}
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '8px' }}>Days Remaining</div>
        </div>
      </section>

      {/* Second Section */}
      <section className="dash-grid dash-grid-mid">
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}><Target size={18}/> Weak Topics</h3>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px', overflowY: 'auto', maxHeight: '250px' }}>
            {data.weak_topics?.slice(0, 4).map((topic: any, idx: number) => (
              <div key={idx} style={{ background: 'rgba(255,23,68,0.1)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--status-critical)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 500 }}>{topic.topic}</span>
                  <span style={{ color: 'var(--status-critical)' }}>{Math.round(topic.mastery * 100)}% Mastery</span>
                </div>
                <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${topic.mastery * 100}%`, background: 'var(--status-critical)' }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--neon-purple)' }}><Clock size={18}/> Today's Mission</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {data.study_plan?.plan?.[0]?.tasks?.map((task: any, idx: number) => (
              <div key={idx} className="timeline-item">
                <div style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{task.topic}</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '4px' }}>
                  Duration: <span style={{ color: 'var(--neon-cyan)' }}>{task.duration}</span>
                </div>
              </div>
            ))}
            <button className="btn-mission" style={{ marginTop: 'auto' }}>INITIATE LEARNING SEQUENCE</button>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--status-ok)' }}><Star size={18}/> Recommendations</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {data.recommendations?.slice(0, 3).map((rec: any, idx: number) => (
              <div key={idx} style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 500 }}>{rec.id_site}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: '4px' }}>Type: {rec.type}</div>
                </div>
                <div style={{ background: 'rgba(0,230,118,0.15)', color: 'var(--status-ok)', padding: '4px 10px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 600 }}>
                  Match: {(rec.score * 100).toFixed(1)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Third Section */}
      <section className="dash-grid dash-grid-bot">
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px' }}>Performance Trend Analysis</h3>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockTrend}>
                <defs>
                  <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--neon-cyan)" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="var(--neon-cyan)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} domain={[50, 100]} />
                <Tooltip contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)', borderRadius: '8px' }} />
                <Area type="monotone" dataKey="score" stroke="var(--neon-cyan)" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px', color: 'var(--neon-purple)' }}>Question Mastery Radar</h3>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart 
                data={Object.entries(data.knowledge?.question_mastery || {}).slice(0, 6).map(([q, m]:any) => ({ name: q, val: m * 100 }))} 
                layout="vertical"
              >
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={80} tick={{fill: 'var(--text-secondary)'}} stroke="none" />
                <Tooltip contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)', borderRadius: '8px' }} cursor={{fill: 'rgba(255,255,255,0.05)'}} />
                <Bar dataKey="val" fill="var(--neon-purple)" radius={[0, 4, 4, 0]}>
                  {Object.entries(data.knowledge?.question_mastery || {}).slice(0, 6).map((_, idx) => (
                    <Cell key={idx} fill={`rgba(157, 0, 255, ${0.4 + idx * 0.1})`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

    </div>
  );
};
