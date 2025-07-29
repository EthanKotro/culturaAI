import React from 'react';
import { Menu, Globe, User, Heart } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const { setSidebarOpen, sidebarOpen, currentLanguage, availableLanguages, setCurrentLanguage, user, isGuest } = useAppStore();

  // const currentLang = availableLanguages.find(lang => lang.code === currentLanguage);

  return (
    <motion.header 
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      className="bg-white shadow-lg border-b-4 border-primary-500 sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and brand */}
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <Menu className="h-6 w-6 text-gray-700" />
            </button>
            
            <motion.div 
              className="flex items-center space-x-3 cursor-pointer"
              whileHover={{ scale: 1.05 }}
              onClick={() => navigate('/')}
            >
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
                <Heart className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Cultura AI</h1>
                <p className="text-xs text-gray-500 hidden sm:block">Preserving African Languages</p>
              </div>
            </motion.div>
          </div>

          {/* Language selector and user menu */}
          <div className="flex items-center space-x-4">
            {/* Language Selector */}
            <div className="relative">
              <select
                value={currentLanguage}
                onChange={(e) => setCurrentLanguage(e.target.value)}
                className="appearance-none bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 pr-8 text-sm font-medium text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
              >
                {availableLanguages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.nativeName}
                  </option>
                ))}
              </select>
              <Globe className="absolute right-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
            </div>

            {/* User menu */}
            <div className="flex items-center space-x-2">
              {isGuest ? (
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-primary-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-600 transition-colors"
                >
                  Sign In
                </motion.button>
              ) : (
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-secondary-500 rounded-full flex items-center justify-center">
                    <User className="h-4 w-4 text-white" />
                  </div>
                  <span className="text-sm font-medium text-gray-700 hidden sm:block">
                    {user?.name}
                  </span>
                  <div className="hidden sm:flex items-center space-x-1 bg-accent-100 px-2 py-1 rounded-full">
                    <span className="text-xs font-bold text-accent-700">{user?.points || 0}</span>
                    <span className="text-xs text-accent-600">pts</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  );
};