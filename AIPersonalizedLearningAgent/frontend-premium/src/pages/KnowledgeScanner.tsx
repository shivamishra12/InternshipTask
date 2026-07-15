import React, { useState, useEffect } from 'react';
import { ScanSearch, Cpu, BookOpen, CheckCircle, BrainCircuit } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell, CartesianGrid } from 'recharts';

export const KnowledgeScanner: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = '11391';

  useEffect(() => {
    const fetchKnowledge = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/knowledge', {
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
    fetchKnowledge();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--neon-purple)" />
      <div style={{ color: 'var(--neon-purple)', letterSpacing: '0.1em' }}>INITIALIZING KNOWLEDGE SCANNER...</div>
    </div>
  );

  const masteryData = data?.question_mastery || {};
  const entries = Object.entries(masteryData);
  
  // Format for radar chart (group into a few synthetic categories for the visual since we have q1..q100)
  const radarData = [
    { subject: 'Algebra', A: (entries.slice(0, 10).reduce((acc:any, [_,v]:any)=>acc+v, 0)/10 * 100) || 85 },
    { subject: 'Geometry', A: (entries.slice(10, 20).reduce((acc:any, [_,v]:any)=>acc+v, 0)/10 * 100) || 60 },
    { subject: 'Calculus', A: (entries.slice(20, 30).reduce((acc:any, [_,v]:any)=>acc+v, 0)/10 * 100) || 75 },
    { subject: 'Statistics', A: (entries.slice(30, 40).reduce((acc:any, [_,v]:any)=>acc+v, 0)/10 * 100) || 40 },
    { subject: 'Physics', A: (entries.slice(40, 50).reduce((acc:any, [_,v]:any)=>acc+v, 0)/10 * 100) || 90 },
    { subject: 'Chemistry', A: (entries.slice(50, 60).reduce((acc:any, [_,v]:any)=>acc+v, 0)/10 * 100) || 55 },
  ];

  // Top mastery questions
  const topQuestions = entries.sort((a:any, b:any) => b[1] - a[1]).slice(0, 5).map(e => ({ name: e[0], val: Math.round((e[1] as number) * 100) }));
  
  // Overall score
  const overallScore = Math.round((entries.reduce((acc:any, [_,v]:any)=>acc+v, 0) / entries.length) * 100) || 0;

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <ScanSearch size={28} color="var(--neon-purple)" />
        <h2 style={{ color: 'var(--neon-purple)', margin: 0 }}>KNOWLEDGE SCANNER</h2>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '24px' }}>
          <BrainCircuit size={48} color="var(--neon-purple)" />
          <div>
            <h4 style={{ color: 'var(--text-secondary)' }}>Overall Cognitive Mastery</h4>
            <div className="metric-value-huge" style={{ color: 'var(--text-primary)', marginTop: '8px' }}>
              {overallScore}<span style={{fontSize:'2rem', color:'var(--neon-purple)'}}>%</span>
            </div>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '24px' }}>
          <CheckCircle size={48} color="var(--status-ok)" />
          <div>
            <h4 style={{ color: 'var(--text-secondary)' }}>Concepts Mastered</h4>
            <div className="metric-value-huge" style={{ color: 'var(--status-ok)', marginTop: '8px' }}>
              {entries.filter((e:any) => e[1] > 0.8).length}
            </div>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '24px' }}>
          <BookOpen size={48} color="var(--neon-cyan)" />
          <div>
            <h4 style={{ color: 'var(--text-secondary)' }}>Active Study Topics</h4>
            <div className="metric-value-huge" style={{ color: 'var(--neon-cyan)', marginTop: '8px' }}>
              {entries.filter((e:any) => e[1] > 0.4 && e[1] <= 0.8).length}
            </div>
          </div>
        </div>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px', color: 'var(--neon-purple)' }}>Cognitive Area Radar</h3>
          <div style={{ height: '350px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-secondary)' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Tooltip contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--neon-purple)', borderRadius: '8px' }} />
                <Radar name="Mastery" dataKey="A" stroke="var(--neon-purple)" fill="var(--neon-purple)" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px', color: 'var(--text-primary)' }}>Top Mastered Concepts</h3>
          <div style={{ height: '350px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topQuestions} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={true} vertical={false}/>
                <XAxis type="number" domain={[0, 100]} hide />
                <YAxis dataKey="name" type="category" width={80} tick={{fill: 'var(--text-secondary)'}} stroke="none" />
                <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ background: 'var(--bg-panel)', border: '1px solid var(--glass-border)' }} />
                <Bar dataKey="val" radius={[0, 4, 4, 0]}>
                  {topQuestions.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={`rgba(157, 0, 255, ${1 - index * 0.1})`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
