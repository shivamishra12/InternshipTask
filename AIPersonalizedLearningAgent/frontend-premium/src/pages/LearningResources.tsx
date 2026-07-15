import React, { useState, useEffect } from 'react';
import { BookOpen, Cpu, Filter, Search, Bookmark, ExternalLink, PlayCircle, FileText, Compass } from 'lucide-react';

export const LearningResources: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const studentId = '11391';

  useEffect(() => {
    const fetchResources = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/recommendations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_id: parseInt(studentId), k: 12 })
        });
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchResources();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
      <Cpu className="animate-spin" size={48} color="var(--status-ok)" />
      <div style={{ color: 'var(--status-ok)', letterSpacing: '0.1em' }}>QUERYING RESOURCE DATABASE...</div>
    </div>
  );

  const recommendations = data?.recommendations || [];

  // Enrich backend data with mock metadata for the UI
  const enrichedResources = recommendations.map((rec:any, idx:number) => ({
    ...rec,
    title: `Advanced Module: Domain ${rec.id_site.toString().slice(-3)}`,
    description: `Targeted learning material based on your recent performance. Addresses common pitfalls in this knowledge domain.`,
    type: idx % 3 === 0 ? 'video' : idx % 2 === 0 ? 'interactive' : 'document',
    difficulty: idx % 4 === 0 ? 'Expert' : idx % 3 === 0 ? 'Intermediate' : 'Beginner',
    time: `${Math.floor(Math.random() * 30 + 15)} min`,
    bookmarked: idx === 1
  }));

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <BookOpen size={28} color="var(--status-ok)" />
          <h2 style={{ color: 'var(--status-ok)', margin: 0 }}>LEARNING RESOURCES</h2>
        </div>
        
        <div style={{ display: 'flex', gap: '12px' }}>
          <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', padding: '6px 16px', gap: '8px', borderRadius: '24px' }}>
            <Search size={16} color="var(--text-secondary)" />
            <input type="text" placeholder="Search database..." style={{ background: 'transparent', border: 'none', color: 'white', width: '200px', outline: 'none' }} />
          </div>
          <button className="glass-panel" style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '6px 16px', borderRadius: '24px', color: 'var(--neon-cyan)', border: '1px solid var(--neon-cyan)', background: 'transparent', cursor: 'pointer' }}>
            <Filter size={16} /> Filters
          </button>
        </div>
      </div>

      <div className="dash-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '24px' }}>
        {enrichedResources.map((res:any, idx:number) => (
          <div key={idx} className="glass-panel" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            {/* Header Image/Type */}
            <div style={{ height: '120px', background: res.type === 'video' ? 'linear-gradient(135deg, rgba(157,0,255,0.2), rgba(0,243,255,0.1))' : 'linear-gradient(135deg, rgba(0,230,118,0.2), rgba(0,102,255,0.1))', position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {res.type === 'video' ? <PlayCircle size={48} color="rgba(255,255,255,0.5)" /> : 
               res.type === 'interactive' ? <Compass size={48} color="rgba(255,255,255,0.5)" /> : 
               <FileText size={48} color="rgba(255,255,255,0.5)" />}
               
              <div style={{ position: 'absolute', top: 12, right: 12, cursor: 'pointer' }}>
                <Bookmark size={20} color={res.bookmarked ? 'var(--status-warn)' : 'rgba(255,255,255,0.5)'} fill={res.bookmarked ? 'var(--status-warn)' : 'none'} />
              </div>
              <div style={{ position: 'absolute', bottom: 12, left: 12, background: 'rgba(0,0,0,0.6)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem', color: 'white', fontWeight: 'bold' }}>
                Match: {(res.score * 100).toFixed(1)}%
              </div>
            </div>

            {/* Content */}
            <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', flex: 1, gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {res.type}
                </span>
                <span style={{ fontSize: '0.75rem', color: res.difficulty === 'Expert' ? 'var(--status-critical)' : res.difficulty === 'Intermediate' ? 'var(--status-warn)' : 'var(--status-ok)', fontWeight: 600 }}>
                  {res.difficulty}
                </span>
              </div>
              
              <h3 style={{ color: 'var(--text-primary)', margin: 0, fontSize: '1.1rem' }}>{res.title}</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', flex: 1 }}>{res.description}</p>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px', paddingTop: '12px', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--neon-cyan)' }}>{res.time}</span>
                <button className="btn-mission" style={{ padding: '6px 12px', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '6px', borderColor: 'var(--status-ok)', color: 'var(--status-ok)' }}>
                  INITIATE <ExternalLink size={14} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
