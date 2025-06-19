import React, { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { TranslationHub } from '../Translation/TranslationHub';
import { StoryExplorer } from '../Stories/StoryExplorer';
import { GameHub } from '../Games/GameHub';
import { useAppStore } from '../../store/useAppStore';

export const Layout: React.FC = () => {
  const { sidebarOpen, setSidebarOpen, currentPage, setCurrentPage } = useAppStore();

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'translate':
        return <TranslationHub />;
      case 'stories':
        return <StoryExplorer />;
      case 'games':
        return <GameHub />;
      case 'profile':
        return <div className="p-6 text-center">Profile page coming soon...</div>;
      case 'settings':
        return <div className="p-6 text-center">Settings page coming soon...</div>;
      case 'help':
        return <div className="p-6 text-center">Help & Support page coming soon...</div>;
      default:
        return <TranslationHub />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 bg-african-pattern">
      <Header />
      
      {sidebarOpen ? (
        <div className="grid grid-cols-[320px_1fr] transition-all duration-300">
          {/* Sidebar */}
          <div className="bg-white shadow-lg">
            <Sidebar onNavigate={setCurrentPage} />
          </div>
          
          {/* Main Content */}
          <main className="overflow-hidden max-w-full px-4 sm:px-6 lg:px-8">
            {renderCurrentPage()}
          </main>
        </div>
      ) : (
        <main className="overflow-hidden max-w-full px-4 sm:px-6 lg:px-8">
          {renderCurrentPage()}
        </main>
      )}
    </div>
  );
};