import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Heart, BookOpen, Users, Languages, Github, Twitter } from 'lucide-react';

const features = [
  {
    icon: <BookOpen className="h-8 w-8 text-primary-500 mb-2" />,
    title: 'Cultural Preservation',
    desc: 'Preserve and share African cultural heritage through stories and translations.',
  },
  {
    icon: <Languages className="h-8 w-8 text-primary-500 mb-2" />,
    title: 'Language Learning',
    desc: 'Learn and translate African languages with AI-powered tools.',
  },
  {
    icon: <Users className="h-8 w-8 text-primary-500 mb-2" />,
    title: 'Community Engagement',
    desc: 'Connect with a community passionate about African culture.',
  },
];

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-yellow-100 via-orange-100 to-pink-100 relative overflow-x-hidden">
      {/* Animated African Pattern Overlay */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.12 }}
          transition={{ duration: 1.5 }}
          className="w-full h-full bg-african-pattern bg-repeat opacity-10 animate-pulse"
        />
      </div>
      {/* Hero Section */}
      <div className="relative flex-1 flex items-center justify-center z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-4xl mx-auto px-4 sm:px-6 lg:px-8"
        >
          <div className="flex flex-col items-center gap-8">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-primary-500 rounded-full flex items-center justify-center shadow-lg">
                <Heart className="h-7 w-7 text-white animate-bounce" />
              </div>
              <div>
                <h1 className="text-5xl font-extrabold text-gray-900 drop-shadow-lg">CulturaAI</h1>
                <p className="text-xl text-primary-700 font-medium mt-1">Preserving African Languages</p>
              </div>
            </div>
            <p className="text-gray-700 text-center max-w-2xl text-lg">
              Welcome to <span className="font-semibold text-primary-600">CulturaAI</span>, where we bridge cultures through language and storytelling.<br />
              Explore African languages, share stories, and connect with a community passionate about cultural preservation.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/stories" className="px-7 py-3 bg-primary-500 text-white rounded-lg font-semibold hover:bg-primary-600 shadow transition-colors">
                Explore Stories
              </Link>
              <Link to="/translation" className="px-7 py-3 bg-white text-primary-700 rounded-lg font-semibold hover:bg-gray-100 border border-primary-200 shadow transition-colors">
                Start Translating
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
      {/* Features Section */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, idx) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 + idx * 0.2 }}
              className="p-8 bg-white rounded-2xl shadow-xl flex flex-col items-center text-center hover:scale-105 transition-transform"
            >
              {feature.icon}
              <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
      {/* Footer */}
      <footer className="w-full bg-primary-50 py-6 mt-auto z-10 border-t border-primary-100">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between px-4 gap-2">
          <div className="text-gray-500 text-sm">© {new Date().getFullYear()} CulturaAI. All rights reserved.</div>
          <div className="flex gap-4">
            <a href="https://github.com/EthanKotro/culturaAI" target="_blank" rel="noopener noreferrer" className="hover:text-primary-600"><Github className="h-5 w-5" /></a>
            <a href="https://twitter.com/" target="_blank" rel="noopener noreferrer" className="hover:text-primary-600"><Twitter className="h-5 w-5" /></a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
