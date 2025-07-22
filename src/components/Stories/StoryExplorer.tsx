import React, { useState, useEffect } from 'react';
import { BookOpen, Play, Pause, Heart, Eye, Star, Filter } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { motion } from 'framer-motion';
import { StoryDetail } from './StoryDetail';

export const StoryExplorer: React.FC = () => {
  const { availableLanguages, setStories, stories } = useAppStore();
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [currentAudio, setCurrentAudio] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedStory, setSelectedStory] = useState<any | null>(null);

  useEffect(() => {
    const fetchStories = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/stories');
        if (!response.ok) {
          throw new Error(`Network HTTP error! status: ${response.status}`);
        }
        const stories_page = await response.json();
        const stories = stories_page.results;
        if (!Array.isArray(stories)) {
          throw new Error('Unexpected response format. Expected an array of stories.');
        }
        setStories(stories);
      } catch (error) {
        console.error('Error fetching stories:', error);
      }
    };
    fetchStories();
  }, [setStories]);

  const categories = ['all', 'wisdom', 'heroic', 'origin', 'romance', 'humor'];
  const difficulties = ['all', 'beginner', 'intermediate', 'advanced'];

  const filteredStories = stories.filter(story => {
    return (selectedLanguage === 'all' || story.language === selectedLanguage) &&
      (selectedCategory === 'all' || story.category === selectedCategory) &&
      (selectedDifficulty === 'all' || story.difficulty === selectedDifficulty);
  });

  const toggleAudio = (storyId: string) => {
    if (currentAudio === storyId && isPlaying) {
      setIsPlaying(false);
    } else {
      setCurrentAudio(storyId);
      setIsPlaying(true);
      // In a real app, this would control actual audio playback
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'wisdom': return '🦉';
      case 'heroic': return '⚔️';
      case 'origin': return '🌱';
      case 'romance': return '💕';
      case 'humor': return '😄';
      default: return '📖';
    }
  };
  if (selectedStory) {
    const storyLang = availableLanguages.find(lang => lang.code === selectedStory.language);
    return (
      <StoryDetail
        story={selectedStory}
        onBack={() => setSelectedStory(null)}
        storyLang={storyLang}
      />
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <h1 className="text-4xl font-bold text-gray-900">Story Explorer</h1>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Discover the rich oral traditions of Kenya through authentic folktales in Kikuyu, Luo, and Kamba languages
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-lg border border-gray-200 p-6"
      >
        <div className="flex items-center space-x-2 mb-4">
          <Filter className="h-5 w-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">Filter Stories</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Language Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Languages</option>
              {availableLanguages.filter(lang => lang.code !== 'en').map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.flag} {lang.name}
                </option>
              ))}
            </select>
          </div>

          {/* Category Filter */}
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

          {/* Difficulty Filter */}
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
        </div>
      </motion.div>

      {/* Stories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredStories.map((story, index) => {
          const storyLang = availableLanguages.find(lang => lang.code === story.language);
          const isCurrentlyPlaying = currentAudio === story.id && isPlaying;

          return (
            <motion.div
              key={story.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.1 }}
              whileHover={{ y: -5 }}
              className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-all cursor-pointer"
              onClick={() => setSelectedStory(story)}
            >
              {/* Story Header */}
              <div className="bg-gradient-to-r from-primary-50 to-accent-50 p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-lg">{getCategoryIcon(story.category)}</span>
                      <span className="text-sm font-medium text-gray-600">
                        {storyLang?.flag} {storyLang?.name}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(story.difficulty)}`}>
                        {story.difficulty}
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 line-clamp-2">
                      {story.title}
                    </h3>
                  </div>

                  <motion.button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleAudio(story.id);
                    }}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className={`p-2 rounded-full transition-colors ${isCurrentlyPlaying
                        ? 'bg-primary-500 text-white'
                        : 'bg-white text-primary-600 hover:bg-primary-50'
                      }`}
                  >
                    {isCurrentlyPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                  </motion.button>
                </div>
              </div>

              {/* Story Content */}
              <div className="p-4">
                <p className="text-gray-600 text-sm line-clamp-3 mb-4">
                  {story.summary}
                </p>

                {/* Story Stats */}
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-1">
                      <Heart className="h-4 w-4" />
                      <span>{story.likes}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Eye className="h-4 w-4" />
                      <span>{story.views}</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 text-yellow-400 fill-current" />
                    <span>4.8</span>
                  </div>
                </div>
              </div>

              {/* Category Badge */}
              <div className="px-4 pb-4">
                <span className="inline-block bg-gray-100 text-gray-800 text-xs font-medium px-2 py-1 rounded-full">
                  {story.category.charAt(0).toUpperCase() + story.category.slice(1)} Tale
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Empty State */}
      {filteredStories.length === 0 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center py-12"
        >
          <BookOpen className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Stories Found</h3>
          <p className="text-gray-600">
            Try adjusting your filters to discover more folktales
          </p>
        </motion.div>
      )}
    </div>
  );
};  