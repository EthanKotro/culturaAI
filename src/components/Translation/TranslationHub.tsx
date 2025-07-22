import React, { useState } from 'react';
import { ArrowLeftRight, Volume2, Copy, History, Mic, Send } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { motion } from 'framer-motion';

export const TranslationHub: React.FC = () => {
  const { availableLanguages, addTranslation, translations, isTranslating, setIsTranslating } = useAppStore();
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('sw');
  const [isListening, setIsListening] = useState(false);

  const handleTranslate = async () => {
    if (!sourceText.trim()) return;
    
    // If source and target languages are the same, just copy the text
    if (sourceLang === targetLang) {
      setTranslatedText(sourceText);
      return;
    }
    
    setIsTranslating(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/translations/translate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source_text: sourceText,
          source_language: sourceLang,
          target_language: targetLang,
        }),
      });

      const data = await response.json();
      
      if (!data.translated_text) {
        console.error('Backend response:', data);
        throw new Error(`Translation failed: ${data.error || 'No translated text received'}`);
      }

      setTranslatedText(data.translated_text);

      const newTranslation = {
        id: data.id.toString(),
        sourceText: data.source_text,
        translatedText: data.translated_text,
        sourceLang: data.source_language,
        targetLang: data.target_language,
        timestamp: new Date(data.created_at),
        modelUsed: data.model_used,
        confidenceScore: data.confidence_score,
        processingTime: data.processing_time,
        userRating: data.user_rating,
        isFavorite: data.is_favorite
      };

      addTranslation(newTranslation);
    } catch (error) {
      console.error('Translation error:', error);
      setTranslatedText('Translation service error');
      
    } finally {
      setIsTranslating(false);
    }
  };

  const swapLanguages = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
    setSourceText(translatedText);
    setTranslatedText(sourceText);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const playAudio = (text: string, lang: string) => {
    // Placeholder for TTS functionality
    console.log(`Playing audio for: ${text} in ${lang}`);
  };

  const startListening = () => {
    setIsListening(true);
    // Placeholder for speech recognition
    setTimeout(() => {
      setIsListening(false);
      setSourceText("Hello, how are you?");
    }, 2000);
  };

  const sourceLangObj = availableLanguages.find(lang => lang.code === sourceLang);
  const targetLangObj = availableLanguages.find(lang => lang.code === targetLang);

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <h1 className="text-4xl font-bold text-gray-900">Translation Hub</h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Bridge languages and cultures with AI-powered translations between English, Kikuyu, Luo, and Kamba
        </p>
      </motion.div>

      {/* Main Translation Interface */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden"
      >
        {/* Language Selector Bar */}
        <div className="bg-gradient-to-r from-primary-50 to-accent-50 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <select
                value={sourceLang}
                onChange={(e) => {
                  setSourceLang(e.target.value);
                  setTranslatedText('');
                }}
                className="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                {availableLanguages.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
              <span className="text-sm text-gray-600">
                {sourceLangObj?.nativeName}
              </span>
            </div>

            <motion.button
              onClick={swapLanguages}
              whileHover={{ scale: 1.1, rotate: 180 }}
              whileTap={{ scale: 0.9 }}
              className="p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-all"
            >
              <ArrowLeftRight className="h-5 w-5 text-primary-600" />
            </motion.button>

            <div className="flex items-center space-x-3">
              <span className="text-sm text-gray-600">
                {targetLangObj?.nativeName}
              </span>
              <select
                value={targetLang}
                onChange={(e) => {
                  setTargetLang(e.target.value);
                  setTranslatedText('');
                }}
                className="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                {availableLanguages.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Translation Areas */}
        <div className="grid md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-gray-200">
          {/* Source Text */}
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">
                From {sourceLangObj?.name}
              </h3>
              <div className="flex items-center space-x-2">
                <motion.button
                  onClick={startListening}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className={`p-2 rounded-lg transition-colors ${
                    isListening 
                      ? 'bg-red-100 text-red-600 animate-pulse' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  <Mic className="h-4 w-4" />
                </motion.button>
              </div>
            </div>
            
            <textarea
              value={sourceText}
              onChange={(e) => setSourceText(e.target.value)}
              placeholder={`Type your text in ${sourceLangObj?.name}...`}
              className="w-full h-40 p-4 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">
                {sourceText.length}/1000 characters
              </span>
              <div className="flex items-center space-x-2">
                {sourceText && (
                  <>
                    <button
                      onClick={() => playAudio(sourceText, sourceLang)}
                      className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
                    >
                      <Volume2 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => copyToClipboard(sourceText)}
                      className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
                    >
                      <Copy className="h-4 w-4" />
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Target Text */}
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">
                To {targetLangObj?.name}
              </h3>
            </div>
            
            <div className="w-full h-40 p-4 bg-gray-50 border border-gray-200 rounded-lg flex items-start">
              {isTranslating ? (
                <div className="flex items-center space-x-2 text-primary-600">
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-primary-600 border-t-transparent"></div>
                  <span className="text-sm">Translating...</span>
                </div>
              ) : translatedText ? (
                <p className="text-gray-900 whitespace-pre-wrap">{translatedText}</p>
              ) : (
                <p className="text-gray-400 text-sm">Translation will appear here...</p>
              )}
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">
                {translatedText.length} characters
              </span>
              <div className="flex items-center space-x-2">
                {translatedText && !isTranslating && (
                  <>
                    <button
                      onClick={() => playAudio(translatedText, targetLang)}
                      className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
                    >
                      <Volume2 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => copyToClipboard(translatedText)}
                      className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
                    >
                      <Copy className="h-4 w-4" />
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Translate Button */}
        <div className="p-6 bg-gray-50 border-t border-gray-200">
          <motion.button
            onClick={handleTranslate}
            disabled={!sourceText.trim() || isTranslating}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full bg-gradient-to-r from-primary-500 to-accent-500 text-white py-3 px-6 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:from-primary-600 hover:to-accent-600 transition-all flex items-center justify-center space-x-2"
          >
            <Send className="h-5 w-5" />
            <span>{isTranslating ? 'Translating...' : 'Translate'}</span>
          </motion.button>
        </div>
      </motion.div>

      {/* Recent Translations */}
      {translations.length > 0 && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl shadow-lg border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-2 mb-4">
            <History className="h-5 w-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-900">Recent Translations</h3>
          </div>
          
          <div className="space-y-3">
            {translations.slice(0, 5).map((translation) => {
              const sourceLangObj = availableLanguages.find(lang => lang.code === translation.sourceLang);
              const targetLangObj = availableLanguages.find(lang => lang.code === translation.targetLang);
              
              return (
                <motion.div
                  key={translation.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors cursor-pointer"
                  onClick={() => {
                    setSourceText(translation.sourceText);
                    setTranslatedText(translation.translatedText);
                    setSourceLang(translation.sourceLang);
                    setTargetLang(translation.targetLang);
                  }}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 space-y-2">
                      <div className="text-sm">
                        <span className="font-medium">{sourceLangObj?.flag} {sourceLangObj?.name}</span>
                        <span className="mx-2 text-gray-400">→</span>
                        <span className="font-medium">{targetLangObj?.flag} {targetLangObj?.name}</span>
                      </div>
                      <div className="text-gray-900">{translation.sourceText}</div>
                      <div className="text-gray-600 text-sm">{translation.translatedText}</div>
                    </div>
                    <div className="text-xs text-gray-400 ml-4">
                      {translation.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      )}
    </div>
  );
};