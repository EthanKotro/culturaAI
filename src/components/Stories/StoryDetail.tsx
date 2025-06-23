import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Heart, Eye, Star } from 'lucide-react';

interface StoryDetailProps {
  story: any;
  onBack: () => void;
  storyLang?: { flag: string; name: string };
}

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

export const StoryDetail: React.FC<StoryDetailProps> = ({ story, onBack, storyLang }) => {
  const [fullStory, setFullStory] = useState<any>(story);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchFullStory = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/stories/${story.id}/`);
        if (!response.ok) throw new Error('Failed to fetch story');
        const data = await response.json();
        setFullStory(data);
      } catch (e) {
        setFullStory(story); // fallback to partial story
      }
      setLoading(false);
    };
    if (story && story.id) {
      fetchFullStory();
    }
  }, [story]);

  if (!story) return null;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-50 to-accent-50 p-4 flex items-center justify-between">
          <button onClick={onBack} className="flex items-center text-primary-600 hover:underline">
            <ArrowLeft className="h-5 w-5 mr-1" /> Back
          </button>
          <div className="flex items-center space-x-2">
            <span className="text-lg">{getCategoryIcon(fullStory.category)}</span>
            <span className="text-sm font-medium text-gray-600">
              {storyLang?.flag} {storyLang?.name}
            </span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(fullStory.difficulty)}`}>
              {fullStory.difficulty}
            </span>
          </div>
        </div>

        {/* Title */}
        <div className="p-6 pb-2">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">{fullStory.title}</h2>
          <p className="text-gray-600 mb-4">{fullStory.summary}</p>
        </div>

        {/* Story Content */}
        <div className="px-6 pb-6">
          <div className="prose max-w-none text-gray-800 mb-6">
            {loading ? (
              <span>Loading story...</span>
            ) : (
              fullStory.content
            )}
          </div>
          {/* Stats */}
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <Heart className="h-4 w-4" />
                <span>{fullStory.likes}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Eye className="h-4 w-4" />
                <span>{fullStory.views}</span>
              </div>
            </div>
            <div className="flex items-center space-x-1">
              <Star className="h-4 w-4 text-yellow-400 fill-current" />
              <span>4.8</span>
            </div>
          </div>
        </div>
        {/* Category Badge */}
        <div className="px-6 pb-6">
          <span className="inline-block bg-gray-100 text-gray-800 text-xs font-medium px-2 py-1 rounded-full">
            {fullStory.category?.charAt(0).toUpperCase() + fullStory.category?.slice(1)} Tale
          </span>
        </div>
      </motion.div>
    </div>
  );
};