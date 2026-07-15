import React, { useState, useEffect } from 'react';
import { ShieldAlert, AlertTriangle, AlertOctagon, Activity, Cpu, ShieldCheck } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';

export const RiskRadar: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = '11391'; // Hardcoded for demo

  useEffect(() => {
    const fetchRisk = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/predict/risk', {
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
    fetchRisk();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--neon-cyan)" />
      <div style={{ color: 'var(--neon-cyan)', letterSpacing: '0.1em' }}>SCANNING FOR MISSION RISKS...</div>
    </div>
  );

  const riskScore = data?.risk_score * 100 || 0;
  const isAtRisk = data?.is_at_risk;
  const statusColor = isAtRisk ? 'var(--status-critical)' : 'var(--status-ok)';
  const statusGlow = isAtRisk ? '0 0 30px rgba(255, 23, 68, 0.4)' : '0 0 30px rgba(0, 230, 118, 0.4)';

  const pieData = [
    { name: 'Risk', value: riskScore },
    { name: 'Safe', value: 100 - riskScore }
  ];
  const pieColors = [statusColor, 'rgba(255,255,255,0.05)'];

  // Mock timeline and actions since backend only gives a boolean and score
  const suggestedActions = isAtRisk ? [
    { action: "Immediate intervention on 'Topic 7'", priority: "CRITICAL" },
    { action: "Assign remedial quiz module", priority: "HIGH" },
    { action: "Schedule 1-on-1 tutoring session", priority: "MEDIUM" }
  ] : [
    { action: "Maintain current study cadence", priority: "LOW" },
    { action: "Unlock advanced challenge modules", priority: "LOW" }
  ];

  const timeline = [
    { day: "T-14", event: "Missed Assignment 3", level: "high" },
    { day: "T-10", event: "Quiz Score dropped 15%", level: "critical" },
    { day: "T-4", event: "Inactive for 3 days", level: "medium" },
    { day: "T-0", event: "Risk Threshold Exceeded", level: "critical" }
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <ShieldAlert size={28} color={statusColor} />
        <h2 style={{ color: statusColor, margin: 0 }}>RISK RADAR</h2>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: '1fr 2fr' }}>
        
        {/* Left: Overall Risk Assessment */}
        <div className="glass-panel" style={{ padding: '32px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', borderColor: statusColor }}>
          <h3 style={{ marginBottom: '24px', color: 'var(--text-secondary)' }}>System Threat Level</h3>
          
          <div style={{ position: 'relative', width: '220px', height: '220px', marginBottom: '24px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} innerRadius={80} outerRadius={100} startAngle={90} endAngle={-270} dataKey="value" stroke="none">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
              {isAtRisk ? <AlertOctagon size={36} color={statusColor} /> : <ShieldCheck size={36} color={statusColor} />}
              <div className="metric-value-huge" style={{ color: statusColor, textShadow: statusGlow, marginTop: '8px', fontSize: '2.5rem' }}>
                {riskScore.toFixed(0)}<span style={{fontSize:'1.5rem'}}>%</span>
              </div>
            </div>
          </div>

          <div style={{ padding: '12px 24px', background: isAtRisk ? 'rgba(255,23,68,0.1)' : 'rgba(0,230,118,0.1)', borderRadius: '24px', color: statusColor, fontWeight: 'bold', letterSpacing: '0.1em' }}>
            {isAtRisk ? 'MISSION AT RISK' : 'TRAJECTORY NOMINAL'}
          </div>

          {data?.risk_factors && (
             <div style={{ marginTop: '32px', width: '100%', textAlign: 'left' }}>
               <h4 style={{ color: 'var(--text-secondary)', marginBottom: '12px' }}>Detected Risk Factors</h4>
               <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
                 {data.risk_factors.map((factor: string, idx: number) => (
                   <li key={idx} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem' }}>
                     <AlertTriangle size={14} color="var(--status-warn)" /> {factor}
                   </li>
                 ))}
               </ul>
             </div>
          )}
        </div>

        {/* Right: Actions and Timeline */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ marginBottom: '20px', color: 'var(--text-primary)' }}>Suggested Mission Corrections</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {suggestedActions.map((action, idx) => (
                <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', borderLeft: `3px solid ${action.priority === 'CRITICAL' ? 'var(--status-critical)' : action.priority === 'HIGH' ? 'var(--status-warn)' : 'var(--status-ok)'}` }}>
                  <span style={{ fontWeight: 500 }}>{action.action}</span>
                  <span style={{ fontSize: '0.75rem', padding: '4px 8px', borderRadius: '4px', background: 'rgba(255,255,255,0.1)', color: 'var(--text-secondary)' }}>
                    {action.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
            <h3 style={{ marginBottom: '24px', color: 'var(--text-primary)' }}>Risk Event Timeline</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', paddingLeft: '12px', borderLeft: '2px solid rgba(255,255,255,0.1)' }}>
              {timeline.map((event, idx) => (
                <div key={idx} style={{ position: 'relative' }}>
                  <div style={{ position: 'absolute', left: '-18px', top: '4px', width: '10px', height: '10px', borderRadius: '50%', background: event.level === 'critical' ? 'var(--status-critical)' : event.level === 'high' ? 'var(--status-warn)' : 'var(--neon-cyan)' }} />
                  <div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start' }}>
                    <span style={{ color: 'var(--neon-cyan)', fontWeight: 600, width: '45px' }}>{event.day}</span>
                    <span style={{ color: 'var(--text-primary)' }}>{event.event}</span>
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
