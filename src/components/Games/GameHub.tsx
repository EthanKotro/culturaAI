import React, { useState } from 'react';
import { Gamepad2, Zap, Target, Brain, Trophy, Play, Star, Clock } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { motion } from 'framer-motion';

interface Game {
  id: string;
  title: string;
  description: string;
  icon: string;
  difficulty: 'easy' | 'medium' | 'hard';
  timeEstimate: string;
  points: number;
  category: string;
  players: number;
  rating: number;
}

export const GameHub: React.FC = () => {
  const { availableLanguages } = useAppStore();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [selectedLanguage, setSelectedLanguage] = useState('all');

  const games: Game[] = [
    {
      id: '1',
      title: 'Word Match Challenge',
      description: 'Match English words with their Kikuyu, Luo, or Kamba translations',
      icon: '🔤',
      difficulty: 'easy',
      timeEstimate: '5-10 min',
      points: 50,
      category: 'vocabulary',
      players: 1245,
      rating: 4.8
    },
    {
      id: '2',
      title: 'Cultural Quiz Master',
      description: 'Test your knowledge of African cultures and languages',
      icon: '🧠',
      difficulty: 'medium',
      timeEstimate: '10-15 min',
      points: 100,
      category: 'culture',
      players: 892,
      rating: 4.7
    },
    {
      id: '3',
      title: 'Speed Translation',
      description: 'Race against time to translate phrases correctly',
      icon: '⚡',
      difficulty: 'hard',
      timeEstimate: '3-5 min',
      points: 150,
      category: 'translation',
      players: 567,
      rating: 4.9
    },
    {
      id: '4',
      title: 'Story Builder',
      description: 'Create folktales using traditional African storytelling elements',
      icon: '📚',
      difficulty: 'medium',
      timeEstimate: '15-20 min',
      points: 200,
      category: 'creativity',
      players: 423,
      rating: 4.6
    },
    {
      id: '5',
      title: 'Pronunciation Practice',
      description: 'Perfect your pronunciation with AI-powered feedback',
      icon: '🎤',
      difficulty: 'easy',
      timeEstimate: '10-12 min',
      points: 75,
      category: 'pronunciation',
      players: 789,
      rating: 4.5
    },
    {
      id: '6',
      title: 'Grammar Guardian',
      description: 'Master grammar rules across different African languages',
      icon: '📝',
      difficulty: 'hard',
      timeEstimate: '20-25 min',
      points: 180,
      category: 'grammar',
      players: 334,
      rating: 4.4
    }
  ];

  const categories = ['all', 'vocabulary', 'culture', 'translation', 'creativity', 'pronunciation', 'grammar'];
  const difficulties = ['all', 'easy', 'medium', 'hard'];

  const filteredGames = games.filter(game => {
    return (selectedCategory === 'all' || game.category === selectedCategory) &&
           (selectedDifficulty === 'all' || game.difficulty === selectedDifficulty);
  });

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyIcon = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return '🟢';
      case 'medium': return '🟡';
      case 'hard': return '🔴';
      default: return '⚪';
    }
  };

  const startGame = (gameId: string) => {
    console.log(`Starting game: ${gameId}`);
    // In a real app, this would navigate to the game or start the game logic
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <div className="flex items-center justify-center space-x-2">
          <Gamepad2 className="h-12 w-12 text-primary-600" />
          <h1 className="text-4xl font-bold text-gray-900">Game Hub</h1>
        </div>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Learn African languages through fun, interactive games designed to make language acquisition engaging and memorable
        </p>
      </motion.div>

      {/* Stats Bar */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-4 gap-4"
      >
        {[
          { icon: Trophy, label: 'Games Played', value: '2,341', color: 'text-yellow-600' },
          { icon: Zap, label: 'Points Earned', value: '15,678', color: 'text-blue-600' },
          { icon: Target, label: 'Accuracy Rate', value: '87%', color: 'text-green-600' },
          { icon: Brain, label: 'Learning Streak', value: '12 days', color: 'text-purple-600' }
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 + index * 0.1 }}
            className="bg-white rounded-xl shadow-lg border border-gray-200 p-4 text-center"
          >
            <stat.icon className={`h-8 w-8 mx-auto mb-2 ${stat.color}`} />
            <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
            <div className="text-sm text-gray-600">{stat.label}</div>
          </motion.div>
        ))}
      </motion.div>

      {/* Filters */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-xl shadow-lg border border-gray-200 p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Filter Games</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {difficulties.map(difficulty => (
                <option key={difficulty} value={difficulty}>
                  {difficulty === 'all' ? 'All Levels' : difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Language Focus</label>
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Languages</option>
              {availableLanguages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.flag} {lang.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </motion.div>

      {/* Games Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredGames.map((game, index) => (
          <motion.div
            key={game.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + index * 0.1 }}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-all"
          >
            {/* Game Header */}
            <div className="bg-gradient-to-r from-primary-50 to-accent-50 p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-3">
                    <span className="text-3xl">{game.icon}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(game.difficulty)}`}>
                      {getDifficultyIcon(game.difficulty)} {game.difficulty}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {game.title}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {game.description}
                  </p>
                </div>
              </div>
            </div>

            {/* Game Details */}
            <div className="p-6">
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Clock className="h-4 w-4" />
                  <span>{game.timeEstimate}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Trophy className="h-4 w-4" />
                  <span>{game.points} points</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Star className="h-4 w-4 text-yellow-400 fill-current" />
                  <span>{game.rating}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span>{game.players.toLocaleString()} players</span>
                </div>
              </div>

              {/* Category Badge */}
              <div className="mb-4">
                <span className="inline-block bg-gray-100 text-gray-800 text-xs font-medium px-2 py-1 rounded-full">
                  {game.category.charAt(0).toUpperCase() + game.category.slice(1)}
                </span>
              </div>

              {/* Play Button */}
              <motion.button
                onClick={() => startGame(game.id)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full bg-gradient-to-r from-primary-500 to-accent-500 text-white py-3 px-6 rounded-lg font-medium hover:from-primary-600 hover:to-accent-600 transition-all flex items-center justify-center space-x-2"
              >
                <Play className="h-5 w-5" />
                <span>Play Now</span>
              </motion.button>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Achievement Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl shadow-lg text-white p-8"
      >
        <div className="text-center space-y-4">
          <Trophy className="h-16 w-16 mx-auto text-yellow-300" />
          <h3 className="text-2xl font-bold">Weekly Challenge</h3>
          <p className="text-primary-100 max-w-2xl mx-auto">
            Complete 5 different games this week to earn the "Language Explorer" badge and unlock exclusive content!
          </p>
          <div className="bg-white bg-opacity-20 rounded-lg p-4 max-w-md mx-auto">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium">Progress</span>
              <span className="text-sm font-bold">3/5 games</span>
            </div>
            <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
              <div className="bg-yellow-300 h-2 rounded-full" style={{ width: '60%' }}></div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};