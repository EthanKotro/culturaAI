import React from 'react';
import { X, Languages, BookOpen, Gamepad2, User, Settings, HelpCircle } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const { sidebarOpen, setSidebarOpen } = useAppStore();

  const menuItems = [
    { id: 'translation', icon: Languages, label: 'Translation Hub', description: 'Translate between languages' },
    { id: 'stories', icon: BookOpen, label: 'Story Explorer', description: 'Discover folktales' },
    { id: 'games', icon: Gamepad2, label: 'Game Hub', description: 'Learn through play' },
    { id: 'profile', icon: User, label: 'Profile', description: 'Your learning journey' },
    { id: 'settings', icon: Settings, label: 'Settings', description: 'Customize your experience' },
    { id: 'help', icon: HelpCircle, label: 'Help & Support', description: 'Get assistance' },
  ];

  const handleNavigate = (pageId: string) => {
    navigate(pageId === 'translation' ? '/translation' : `/${pageId}`);
    setSidebarOpen(false);
  };

  return (
    <AnimatePresence>
      {sidebarOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSidebarOpen(false)}
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          />
          
          {/* Sidebar */}
          <motion.div
            initial={{ x: -320 }}
            animate={{ x: 0 }}
            exit={{ x: -320 }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed top-20 bottom-0 left-0 w-80 bg-white shadow-2xl z-50 lg:fixed lg:translate-x-0 lg:shadow-lg"
          >
            <div className="flex flex-col h-full overflow-y-auto custom-scrollbar">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Navigation</h2>
                <button
                  onClick={() => setSidebarOpen(false)}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors lg:hidden "
                >
                  <X className="h-5 w-5 text-gray-500" />
                </button>
              </div>

              {/* Menu Items */}
              <div className="flex-1 overflow-y-auto py-4">
                <nav className="space-y-2 px-4">
                  {menuItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = (item.id === 'translation' && location.pathname === '/translation') ||
                                     (item.id !== 'translation' && location.pathname === `/${item.id}`);
                    
                    return (
                      <motion.button
                        key={item.id}
                        onClick={() => handleNavigate(item.id)}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 text-left ${
                          isActive
                            ? 'bg-primary-50 text-primary-700 border-2 border-primary-200'
                            : 'hover:bg-gray-50 text-gray-700 border-2 border-transparent'
                        }`}
                      >
                        <Icon className={`h-5 w-5 ${isActive ? 'text-primary-600' : 'text-gray-400'}`} />
                        <div className="flex-1">
                          <div className={`font-medium ${isActive ? 'text-primary-800' : 'text-gray-900'}`}>
                            {item.label}
                          </div>
                          <div className="text-xs text-gray-500 mt-0.5">
                            {item.description}
                          </div>
                        </div>
                      </motion.button>
                    );
                  })}
                </nav>
              </div>

              {/* Footer */}
              <div className="p-4 border-t border-gray-200">
                <div className="bg-gradient-to-r from-primary-50 to-accent-50 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-gray-900">Cultural Impact</h3>
                  <p className="text-xs text-gray-600 mt-1">
                    Supporting SDG 4: Quality Education through language preservation
                  </p>
                  <div className="flex items-center mt-2 space-x-2">
                    <div className="w-2 h-2 bg-secondary-500 rounded-full animate-pulse-slow"></div>
                    <span className="text-xs text-secondary-700 font-medium">Actively preserving languages</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};