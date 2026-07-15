import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Brain, Cpu, Crosshair, CheckCircle, Database } from 'lucide-react';

const QUESTIONS = [
  {
    id: 1,
    text: "Which learning environment yields the highest knowledge retention for you?",
    options: ["Visual Diagrams & Charts", "Interactive Simulations", "Text-Based Manuals", "Audio Briefings"]
  },
  {
    id: 2,
    text: "How do you typically approach a complex, multi-variable problem?",
    options: ["Deconstruct into smaller tasks", "Search for historical patterns", "Trial and error execution", "Consult documentation first"]
  },
  {
    id: 3,
    text: "What is your target objective for this mission module?",
    options: ["Achieve maximum mastery (95%+)", "Pass the baseline requirements", "Rapid completion", "Deep theoretical understanding"]
  }
];

export const Assessment: React.FC = () => {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [calibrating, setCalibrating] = useState(false);
  const [calibrationPhase, setCalibrationPhase] = useState(0);
  const navigate = useNavigate();

  const handleSelect = (option: string) => {
    const newAnswers = [...answers, option];
    setAnswers(newAnswers);
    
    if (step < QUESTIONS.length - 1) {
      setStep(step + 1);
    } else {
      startCalibration();
    }
  };

  const startCalibration = () => {
    setCalibrating(true);
    
    // Simulate AI calibration sequence
    setTimeout(() => setCalibrationPhase(1), 1500); // Processing responses
    setTimeout(() => setCalibrationPhase(2), 3000); // Building predictive model
    setTimeout(() => setCalibrationPhase(3), 4500); // Finalizing
    setTimeout(() => {
      // Complete onboarding
      localStorage.setItem('pla_onboarding_completed', 'true');
      // Assign the baseline persona student ID 11391 so the backend doesn't break
      localStorage.setItem('pla_student_id', '11391');
      navigate('/');
    }, 6000);
  };

  if (calibrating) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-space-dark)', gap: '24px' }}>
        <div style={{ position: 'relative', width: 120, height: 120 }}>
          <Cpu size={120} color="var(--neon-cyan)" className="animate-spin" style={{ animationDuration: '3s' }} />
          <Brain size={48} color="var(--neon-purple)" style={{ position: 'absolute', top: 36, left: 36 }} />
        </div>
        
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ color: 'var(--neon-cyan)', letterSpacing: '0.1em', marginBottom: '16px' }}>CALIBRATING NEURAL PROFILE</h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'flex-start', width: '300px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: calibrationPhase >= 0 ? 'var(--status-ok)' : 'var(--text-muted)' }}>
              {calibrationPhase > 0 ? <CheckCircle size={16} /> : <Database size={16} />} 
              <span>Parsing baseline cognitive metrics...</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: calibrationPhase >= 1 ? 'var(--status-ok)' : 'var(--text-muted)' }}>
              {calibrationPhase > 1 ? <CheckCircle size={16} /> : <Database size={16} />} 
              <span>Generating predictive risk threshold...</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: calibrationPhase >= 2 ? 'var(--status-ok)' : 'var(--text-muted)' }}>
              {calibrationPhase > 2 ? <CheckCircle size={16} /> : <Database size={16} />} 
              <span>Aligning personalized mission vectors...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const currentQuestion = QUESTIONS[step];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-space-dark)' }}>
      <div className="glass-panel animate-fade-in" style={{ padding: '48px', width: '100%', maxWidth: '600px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--glass-border)', paddingBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Crosshair size={24} color="var(--neon-cyan)" />
            <span style={{ color: 'var(--neon-cyan)', fontWeight: 600, letterSpacing: '0.1em' }}>INITIAL ASSESSMENT</span>
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Phase {step + 1} of {QUESTIONS.length}
          </div>
        </div>

        <div>
          <h2 style={{ color: 'var(--text-primary)', fontSize: '1.5rem', marginBottom: '24px', lineHeight: 1.4 }}>
            {currentQuestion.text}
          </h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {currentQuestion.options.map((option, idx) => (
              <button 
                key={idx}
                onClick={() => handleSelect(option)}
                className="btn-mission"
                style={{ 
                  padding: '16px 24px', 
                  textAlign: 'left', 
                  fontSize: '1.1rem', 
                  background: 'rgba(0,243,255,0.05)',
                  border: '1px solid rgba(0,243,255,0.2)',
                  color: 'white',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '16px'
                }}
              >
                <div style={{ width: '24px', height: '24px', borderRadius: '50%', border: '1px solid var(--neon-cyan)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', color: 'var(--neon-cyan)' }}>
                  {String.fromCharCode(65 + idx)}
                </div>
                {option}
              </button>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};
