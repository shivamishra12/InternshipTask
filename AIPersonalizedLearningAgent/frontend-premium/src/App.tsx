import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { PerformanceEngine } from './pages/PerformanceEngine';
import { RiskRadar } from './pages/RiskRadar';
import { KnowledgeScanner } from './pages/KnowledgeScanner';
import { WeakTopicAnalyzer } from './pages/WeakTopicAnalyzer';
import { LearningResources } from './pages/LearningResources';
import { MissionPlanner } from './pages/MissionPlanner';
import { AnalyticsCenter } from './pages/AnalyticsCenter';
import { StudentProfile } from './pages/StudentProfile';
import { Settings } from './pages/Settings';
import { Login } from './pages/Login';
import { Signup } from './pages/Signup';
import { Assessment } from './pages/Assessment';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Auth & Onboarding Flow */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/assessment" element={<Assessment />} />

        {/* Protected Dashboard Routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="performance" element={<PerformanceEngine />} />
          <Route path="risk" element={<RiskRadar />} />
          <Route path="knowledge" element={<KnowledgeScanner />} />
          <Route path="weak-topics" element={<WeakTopicAnalyzer />} />
          <Route path="resources" element={<LearningResources />} />
          <Route path="planner" element={<MissionPlanner />} />
          <Route path="analytics" element={<AnalyticsCenter />} />
          <Route path="profile" element={<StudentProfile />} />
          <Route path="settings" element={<Settings />} />
        </Route>
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
