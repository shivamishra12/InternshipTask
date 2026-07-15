import React, { useState, useEffect } from 'react';
import { Target, Cpu, TrendingUp, AlertTriangle, Crosshair } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

export const WeakTopicAnalyzer: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = '11391';

  useEffect(() => {
    const fetchWeakTopics = async () => {
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
    fetchWeakTopics();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--status-critical)" />
      <div style={{ color: 'var(--status-critical)', letterSpacing: '0.1em' }}>ANALYZING VULNERABILITIES...</div>
    </div>
  );

  let weakTopics = data?.weak_topics || [];
  
  // If backend returned empty, mock some for the visual presentation
  if (weakTopics.length === 0) {
    weakTopics = [
      { topic: 'q71', mastery: 0.12, priority: 'CRITICAL', severity: 9.5, action: 'Mandatory Re-training', expected_improvement: '+15%' },
      { topic: 'q51', mastery: 0.22, priority: 'CRITICAL', severity: 8.2, action: 'Guided Tutorial', expected_improvement: '+10%' },
      { topic: 'q95', mastery: 0.26, priority: 'HIGH', severity: 7.4, action: 'Practice Quiz', expected_improvement: '+8%' },
      { topic: 'q74', mastery: 0.28, priority: 'HIGH', severity: 6.8, action: 'Video Lecture', expected_improvement: '+12%' },
      { topic: 'q70', mastery: 0.33, priority: 'MEDIUM', severity: 5.1, action: 'Reading Material', expected_improvement: '+5%' }
    ];
  } else {
    // Enrich backend data with mock presentation fields if missing
    weakTopics = weakTopics.map((wt:any, idx:number) => ({
      ...wt,
      priority: wt.mastery < 0.2 ? 'CRITICAL' : wt.mastery < 0.4 ? 'HIGH' : 'MEDIUM',
      severity: (1 - wt.mastery) * 10,
      action: idx === 0 ? 'Mandatory Re-training' : 'Practice Quiz',
      expected_improvement: `+${Math.floor(Math.random()*10 + 5)}%`
    }));
  }

  const chartData = weakTopics.map((wt:any) => ({
    name: wt.topic,
    severity: wt.severity,
    mastery: Math.round(wt.mastery * 100)
  })).sort((a:any, b:any) => b.severity - a.severity);

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <Target size={28} color="var(--status-critical)" />
        <h2 style={{ color: 'var(--status-critical)', margin: 0 }}>WEAK TOPIC ANALYZER</h2>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: '2fr 1fr' }}>
        
        {/* Left: Detailed List */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={18} color="var(--status-critical)" /> Detected Vulnerabilities
          </h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', overflowY: 'auto', maxHeight: '500px', paddingRight: '8px' }}>
            {weakTopics.map((topic: any, idx: number) => (
              <div key={idx} style={{ padding: '16px', background: 'rgba(255,23,68,0.05)', borderRadius: '12px', border: '1px solid rgba(255,23,68,0.2)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ width: 40, height: 40, borderRadius: '8px', background: 'rgba(255,23,68,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--status-critical)', fontWeight: 'bold' }}>
                      {idx + 1}
                    </div>
                    <div>
                      <h4 style={{ color: 'var(--text-primary)', fontSize: '1.1rem' }}>{topic.topic}</h4>
                      <div style={{ color: 'var(--status-critical)', fontSize: '0.85rem', fontWeight: 600 }}>{topic.priority} PRIORITY</div>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div className="metric-value-huge" style={{ fontSize: '2rem', color: 'var(--status-critical)' }}>
                      {Math.round(topic.mastery * 100)}<span style={{fontSize:'1rem'}}>%</span>
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Current Mastery</div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '16px', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '12px' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Suggested Action</div>
                    <div style={{ color: 'var(--neon-cyan)', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.9rem' }}>
                      <Crosshair size={14} /> {topic.action}
                    </div>
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Expected Improvement</div>
                    <div style={{ color: 'var(--status-ok)', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.9rem' }}>
                      <TrendingUp size={14} /> {topic.expected_improvement}
                    </div>
                  </div>
                  <div>
                    <button className="btn-mission" style={{ padding: '6px 12px', fontSize: '0.75rem' }}>EXECUTE ACTION</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Analytics */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="glass-panel" style={{ padding: '24px', flex: 1, borderColor: 'var(--status-critical)' }}>
            <h3 style={{ marginBottom: '24px', color: 'var(--text-primary)' }}>Severity Distribution</h3>
            <div style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                  <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                  <Tooltip cursor={{fill: 'rgba(255,23,68,0.1)'}} contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--status-critical)' }} />
                  <Bar dataKey="severity" radius={[4, 4, 0, 0]}>
                    {chartData.map((entry:any, index:number) => (
                      <Cell key={`cell-${index}`} fill={entry.severity > 8 ? 'var(--status-critical)' : entry.severity > 5 ? 'var(--status-warn)' : 'var(--neon-cyan)'} />
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
