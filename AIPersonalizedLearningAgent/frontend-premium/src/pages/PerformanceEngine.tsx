import React, { useState, useEffect } from 'react';
import { Activity, Target, Zap, Cpu, TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';

export const PerformanceEngine: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = localStorage.getItem('pla_student_id') || '11391';
  
  // Interactive mock states
  const [studyHours, setStudyHours] = useState(15);
  const [quizScore, setQuizScore] = useState(78);
  const [simulatedProb, setSimulatedProb] = useState<number | null>(null);
  const [isRecalculating, setIsRecalculating] = useState(false);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/predict/performance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_id: parseInt(studentId) })
        });
        const result = await response.json();
        setData(result);
        setSimulatedProb(result.success_probability * 100);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchPrediction();
  }, []);

  const handleRecalculate = async () => {
    setIsRecalculating(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/predict/performance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          student_id: parseInt(studentId),
          study_hours: studyHours,
          quiz_score: quizScore
        })
      });
      const result = await response.json();
      setData(result);
      setSimulatedProb(result.success_probability * 100);
    } catch (err) {
      console.error(err);
    } finally {
      setIsRecalculating(false);
    }
  };

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--neon-cyan)" />
      <div style={{ color: 'var(--neon-cyan)', letterSpacing: '0.1em' }}>INITIALIZING PERFORMANCE ENGINE...</div>
    </div>
  );

  const mockTrend = [
    { name: 'T-5', score: 65 }, { name: 'T-4', score: 68 }, { name: 'T-3', score: 72 }, 
    { name: 'T-2', score: 75 }, { name: 'T-1', score: 73 }, { name: 'T-0', score: simulatedProb ? Math.round(simulatedProb) : 0 }
  ];

  const featureImportance = [
    { feature: 'Recent Quiz Scores', weight: 85 },
    { feature: 'Study Hours Logged', weight: 72 },
    { feature: 'Module Completion Rate', weight: 64 },
    { feature: 'Engagement Score', weight: 48 },
    { feature: 'Previous Exam Performance', weight: 35 },
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <Activity size={28} color="var(--neon-cyan)" />
        <h2 style={{ color: 'var(--neon-cyan)', margin: 0 }}>PERFORMANCE ENGINE</h2>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: '1fr 2fr' }}>
        {/* Left Column: Interactive Simulation */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ marginBottom: '20px', color: 'var(--text-primary)' }}>Simulation Parameters</h3>
            
            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-secondary)' }}>
                <span>Weekly Study Hours</span>
                <span style={{ color: 'var(--neon-cyan)' }}>{studyHours}h</span>
              </label>
              <input 
                type="range" min="0" max="40" value={studyHours} 
                onChange={(e) => setStudyHours(parseInt(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--neon-cyan)' }} 
              />
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-secondary)' }}>
                <span>Avg Quiz Score</span>
                <span style={{ color: 'var(--neon-cyan)' }}>{quizScore}%</span>
              </label>
              <input 
                type="range" min="0" max="100" value={quizScore} 
                onChange={(e) => setQuizScore(parseInt(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--neon-cyan)' }} 
              />
            </div>

            <button 
              onClick={handleRecalculate}
              disabled={isRecalculating}
              className="btn-mission" 
              style={{ width: '100%', display: 'flex', justifyContent: 'center', gap: '8px', opacity: isRecalculating ? 0.5 : 1, cursor: isRecalculating ? 'wait' : 'pointer' }}
            >
              <Zap size={18} /> {isRecalculating ? 'PROCESSING...' : 'RECALCULATE PREDICTION'}
            </button>
          </div>

          <div className="glass-panel" style={{ padding: '24px', textAlign: 'center' }}>
            <h3 style={{ marginBottom: '16px', color: 'var(--text-secondary)' }}>Live Prediction Output</h3>
            <div className="metric-value-huge" style={{ color: 'var(--neon-cyan)', fontSize: '4rem', textShadow: '0 0 30px rgba(0, 243, 255, 0.4)' }}>
              {simulatedProb ? simulatedProb.toFixed(1) : 0}<span style={{fontSize:'2rem'}}>%</span>
            </div>
            <div style={{ color: 'var(--status-ok)', marginTop: '12px', fontWeight: 600, fontSize: '1.1rem', letterSpacing: '0.1em' }}>
              {data?.predicted_performance.toUpperCase()} LIKELY
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '16px' }}>
              Confidence Level: {(data?.confidence_interval?.[0] * 100)?.toFixed(1)}% - {(data?.confidence_interval?.[1] * 100)?.toFixed(1)}%
            </div>
          </div>
        </div>

        {/* Right Column: Charts */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
            <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <TrendingUp size={18} color="var(--neon-cyan)"/> Historical Prediction Trend
            </h3>
            <div style={{ height: '220px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={mockTrend}>
                  <defs>
                    <linearGradient id="colorTrend" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--neon-cyan)" stopOpacity={0.6}/>
                      <stop offset="95%" stopColor="var(--neon-cyan)" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                  <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} domain={[40, 100]} />
                  <Tooltip contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)', borderRadius: '8px' }} />
                  <Area type="monotone" dataKey="score" stroke="var(--neon-cyan)" strokeWidth={3} fill="url(#colorTrend)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
            <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Target size={18} color="var(--neon-purple)"/> Algorithm Feature Importance
            </h3>
            <div style={{ height: '200px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={featureImportance} layout="vertical" margin={{ left: 40 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="feature" type="category" width={150} tick={{fill: 'var(--text-secondary)', fontSize: 12}} stroke="none" />
                  <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)' }} />
                  <Bar dataKey="weight" radius={[0, 4, 4, 0]}>
                    {featureImportance.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={`rgba(0, 243, 255, ${1 - index * 0.15})`} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
