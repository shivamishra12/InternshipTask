import React, { useState, useEffect } from 'react';
import { BarChart2, Cpu, Download } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export const AnalyticsCenter: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = '11391';

  useEffect(() => {
    const fetchAnalytics = async () => {
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
    fetchAnalytics();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--neon-cyan)" />
      <div style={{ color: 'var(--neon-cyan)', letterSpacing: '0.1em' }}>PROCESSING ANALYTICS TELEMETRY...</div>
    </div>
  );

  const baseProb = (data?.performance?.success_probability || 0.8) * 100;
  
  // Mock data over 6 weeks
  const performanceTrends = [
    { week: 'W1', performance: 65, risk: 40, learningTime: 12 },
    { week: 'W2', performance: 68, risk: 35, learningTime: 15 },
    { week: 'W3', performance: 70, risk: 38, learningTime: 14 },
    { week: 'W4', performance: 75, risk: 25, learningTime: 18 },
    { week: 'W5', performance: 73, risk: 28, learningTime: 16 },
    { week: 'W6 (Now)', performance: Math.round(baseProb), risk: (data?.risk?.risk_score || 0)*100, learningTime: 20 },
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <BarChart2 size={28} color="var(--neon-cyan)" />
          <h2 style={{ color: 'var(--neon-cyan)', margin: 0 }}>ANALYTICS CENTER</h2>
        </div>
        <button className="glass-panel" style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', borderRadius: '4px', color: 'var(--text-primary)', border: '1px solid var(--glass-border)', cursor: 'pointer' }}>
          <Download size={16} /> Export Telemetry
        </button>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
        <div className="glass-panel" style={{ padding: '24px', gridColumn: '1 / span 2' }}>
          <h3 style={{ marginBottom: '24px' }}>Performance vs Risk Trend (6 Weeks)</h3>
          <div style={{ height: '350px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={performanceTrends}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="week" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis yAxisId="left" stroke="var(--neon-cyan)" tick={{fill: 'var(--neon-cyan)'}} domain={[0, 100]} />
                <YAxis yAxisId="right" orientation="right" stroke="var(--status-critical)" tick={{fill: 'var(--status-critical)'}} domain={[0, 100]} />
                <Tooltip contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)', borderRadius: '8px' }} />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="performance" name="Performance (%)" stroke="var(--neon-cyan)" strokeWidth={3} dot={{r: 4}} activeDot={{r: 8}} />
                <Line yAxisId="right" type="monotone" dataKey="risk" name="Risk Level (%)" stroke="var(--status-critical)" strokeWidth={3} dot={{r: 4}} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px', color: 'var(--neon-purple)' }}>Weekly Learning Volume (Hrs)</h3>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={performanceTrends}>
                <defs>
                  <linearGradient id="colorTime" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--neon-purple)" stopOpacity={0.6}/>
                    <stop offset="95%" stopColor="var(--neon-purple)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="week" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <Tooltip contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)' }} />
                <Area type="monotone" dataKey="learningTime" stroke="var(--neon-purple)" strokeWidth={3} fill="url(#colorTime)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px', color: 'var(--status-ok)' }}>Knowledge Growth Velocity</h3>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={performanceTrends.map(d => ({ ...d, growth: d.performance * 0.8 + Math.random()*5 }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="week" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <Tooltip contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)' }} />
                <Line type="stepAfter" dataKey="growth" name="Knowledge Index" stroke="var(--status-ok)" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
