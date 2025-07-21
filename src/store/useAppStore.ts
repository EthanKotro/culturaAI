import { create } from 'zustand';

export interface Language {
  code: string;
  name: string;
  nativeName: string;
  flag: string;
}

export interface Translation {
  id: string;
  sourceText: string;
  translatedText: string;
  sourceLang: string;
  targetLang: string;
  timestamp: Date;
}

export interface Story {
  summary: string;
  id: string;
  title: string;
  content: string;
  language: string;
  audioUrl?: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  likes: number;
  views: number;
}

export interface User {
  id: string;
  name: string;
  email: string;
  preferredLanguage: string;
  points: number;
  level: number;
}

interface AppState {
  // Language settings
  currentLanguage: string;
  availableLanguages: Language[];
  
  // Translation
  translations: Translation[];
  isTranslating: boolean;
  
  // Stories
  stories: Story[];
  currentStory: Story | null;
  
  // User
  user: User | null;
  isGuest: boolean;
  
  // UI state
  sidebarOpen: boolean;
  currentPage: string;
  
  // Actions
  setCurrentLanguage: (lang: string) => void;
  addTranslation: (translation: Translation) => void;
  setIsTranslating: (loading: boolean) => void;
  setStories: (stories: Story[]) => void;
  setCurrentStory: (story: Story | null) => void;
  setUser: (user: User | null) => void;
  setIsGuest: (isGuest: boolean) => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  currentLanguage: 'en',
  availableLanguages: [
    { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸' },
    { code: 'ki', name: 'Kikuyu', nativeName: 'Gĩkũyũ', flag: '🇰🇪' },
    { code: 'luo', name: 'Luo', nativeName: 'Dholuo', flag: '🇰🇪' },
    { code: 'kam', name: 'Kamba', nativeName: 'Kikamba', flag: '🇰🇪' },
    { code: 'sw', name: 'Swahili', nativeName: 'Kiswahili', flag: '🇰🇪' },
    { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷'},
    { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸' },
    { code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪' },
    { code: 'it', name: 'Italian', nativeName: 'Italiano', flag: '🇮🇹' },

  ],
  translations: [],
  isTranslating: false,
  stories: [],
  currentStory: null,
  user: null,
  isGuest: true,
  sidebarOpen: false,
  currentPage: 'translate',
  
  // Actions
  setCurrentLanguage: (lang) => set({ currentLanguage: lang }),
  addTranslation: (translation) => set((state) => ({ 
    translations: [translation, ...state.translations.slice(0, 9)] 
  })),
  setIsTranslating: (loading) => set({ isTranslating: loading }),
  setStories: (stories) => set({ stories }),
  setCurrentStory: (story) => set({ currentStory: story }),
  setUser: (user) => set({ user, isGuest: !user }),
  setIsGuest: (isGuest) => set({ isGuest }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
}));