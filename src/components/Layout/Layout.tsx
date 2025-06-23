import React from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { TranslationHub } from '../Translation/TranslationHub';
import { StoryExplorer } from '../Stories/StoryExplorer';
import { GameHub } from '../Games/GameHub';
import { useAppStore } from '../../store/useAppStore';
import { Navigate, Route, Routes } from 'react-router-dom';

export const Layout: React.FC = () => {
  const { sidebarOpen } = useAppStore();
  
  return (
    <div className="min-h-screen bg-gray-50 bg-african-pattern">
      <Header />
      
      {sidebarOpen ? (
        <div className="grid grid-cols-[320px_1fr] transition-all duration-300">
          {/* Sidebar */}
          <div className="bg-white shadow-lg">
            <Sidebar />
          </div>
          
          {/* Main Content */}
          <main className="overflow-hidden max-w-full px-4 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<TranslationHub />} />
              <Route path="/stories" element={<StoryExplorer />} />
              <Route path="/games" element={<GameHub />} />
              <Route path="/profile" element={<div>Profile Page</div>} />
              <Route path="/settings" element={<div>Settings Page</div>} />
              <Route path="/help" element={<div>Help Page</div>} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      ) : (
        <main className="overflow-hidden max-w-full px-4 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<TranslationHub />} />
              <Route path="/stories" element={<StoryExplorer />} />
              <Route path="/games" element={<GameHub />} />
              <Route path="/profile" element={<div>Profile Page</div>} />
              <Route path="/settings" element={<div>Settings Page</div>} />
              <Route path="/help" element={<div>Help Page</div>} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </main>
      )}
    </div>
  );
};