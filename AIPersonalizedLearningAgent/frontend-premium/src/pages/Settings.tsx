import React, { useState } from 'react';
import { Settings as SettingsIcon, Bell, Shield, Monitor, Smartphone, Moon, Sun, Save } from 'lucide-react';

export const Settings: React.FC = () => {
  const [theme, setTheme] = useState('dark');
  const [notifications, setNotifications] = useState({
    missionAlerts: true,
    studyReminders: true,
    systemUpdates: false
  });

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <SettingsIcon size={28} color="var(--text-primary)" />
        <h2 style={{ color: 'var(--text-primary)', margin: 0 }}>SYSTEM PREFERENCES</h2>
      </div>

      <div className="glass-panel" style={{ padding: '32px' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '24px', borderBottom: '1px solid var(--glass-border)', paddingBottom: '12px' }}>
          <Monitor size={20} color="var(--neon-cyan)" /> Interface Configuration
        </h3>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div>
            <div style={{ fontWeight: 600 }}>Visual Theme</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Select NASA Mission Control or Light Mode (Disabled)</div>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button 
              onClick={() => setTheme('dark')}
              style={{ padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '8px', background: theme === 'dark' ? 'rgba(0,243,255,0.1)' : 'transparent', border: `1px solid ${theme === 'dark' ? 'var(--neon-cyan)' : 'var(--glass-border)'}`, color: theme === 'dark' ? 'var(--neon-cyan)' : 'var(--text-secondary)', borderRadius: '4px', cursor: 'pointer' }}>
              <Moon size={16} /> Space Dark
            </button>
            <button 
              onClick={() => setTheme('light')}
              disabled
              style={{ padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '8px', background: 'transparent', border: '1px solid var(--glass-border)', color: 'var(--text-muted)', borderRadius: '4px', cursor: 'not-allowed', opacity: 0.5 }}>
              <Sun size={16} /> Earth Light
            </button>
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '32px' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '24px', borderBottom: '1px solid var(--glass-border)', paddingBottom: '12px' }}>
          <Bell size={20} color="var(--neon-purple)" /> Communication Protocol
        </h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}>
            <div>
              <div style={{ fontWeight: 600 }}>Mission Critical Alerts</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Push notifications for risk threshold breaches</div>
            </div>
            <input type="checkbox" checked={notifications.missionAlerts} onChange={(e) => setNotifications({...notifications, missionAlerts: e.target.checked})} style={{ width: '20px', height: '20px', accentColor: 'var(--neon-cyan)' }} />
          </label>

          <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}>
            <div>
              <div style={{ fontWeight: 600 }}>Study Reminders</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Daily pings for your learning timeline</div>
            </div>
            <input type="checkbox" checked={notifications.studyReminders} onChange={(e) => setNotifications({...notifications, studyReminders: e.target.checked})} style={{ width: '20px', height: '20px', accentColor: 'var(--neon-cyan)' }} />
          </label>

          <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}>
            <div>
              <div style={{ fontWeight: 600 }}>System Updates</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Log of backend model redeployments</div>
            </div>
            <input type="checkbox" checked={notifications.systemUpdates} onChange={(e) => setNotifications({...notifications, systemUpdates: e.target.checked})} style={{ width: '20px', height: '20px', accentColor: 'var(--neon-cyan)' }} />
          </label>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '32px' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '24px', borderBottom: '1px solid var(--glass-border)', paddingBottom: '12px', color: 'var(--status-warn)' }}>
          <Shield size={20} color="var(--status-warn)" /> Privacy & Security
        </h3>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div style={{ fontWeight: 600 }}>Telemetry Data Collection</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Allow SpaceEd Corp to use your anonymous data for AI training</div>
          </div>
          <button className="btn-mission" style={{ borderColor: 'var(--status-warn)', color: 'var(--status-warn)' }}>REVOKE ACCESS</button>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '12px' }}>
        <button className="btn-mission" style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 24px', fontSize: '1rem' }}>
          <Save size={18} /> SAVE PREFERENCES
        </button>
      </div>

    </div>
  );
};
