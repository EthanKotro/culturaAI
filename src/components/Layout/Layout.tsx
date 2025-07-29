import React, { useRef, useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { TranslationHub } from '../Translation/TranslationHub';
import { StoryExplorer } from '../Stories/StoryExplorer';
import { GameHub } from '../Games/GameHub';
import { useAppStore } from '../../store/useAppStore';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { TbMessageChatbotFilled } from 'react-icons/tb';
import axios from 'axios';
import { RxCross2 } from 'react-icons/rx';
import LandingPage from '../LandingPage/LandingPage';
import ProfilePage from '../Profile/ProfilePage';
import SettingsPage from '../Settings/SettingsPage';
import { MdFullscreen, MdOutlineFullscreenExit } from 'react-icons/md';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

export const Layout: React.FC = () => {
  const location = useLocation();
  const { sidebarOpen } = useAppStore();
  const [ chatbotOpen, setChatbotOpen ] = useState(false);
  const [ chatbotOpenFullScreen, setChatbotOpenFullScreen ] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    { sender: 'bot', text: 'Hi! How can I help you today?' },
    { sender: 'user', text: 'What is the weather like in Nairobi?' },
    { sender: 'bot', text: 'Today in Nairobi it’s sunny with a high of 27°C.' },
  ]);

  const [inputValue, setInputValue] = useState('');
  const chatHistoryRef = useRef<HTMLDivElement | null>(null);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    // setMessages([...messages, { sender: 'user', text: inputValue.trim() }]);
    const userMsg: Message = { sender: 'user', text: inputValue.trim() };
    setMessages((prev) => [...prev, userMsg])
    setInputValue('');

    try{
      const response = await axios.post("http://localhost:8000/api/v1/chatbot/", {
        message:inputValue.trim(),
      });

      const botReply: Message = { sender: 'bot', text: response.data.reply };
      setMessages((prev) => [...prev, botReply]);
      
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [...prev, { sender: 'bot', text: 'Oops, failed to reach the server.' }]);
    }

    // Auto-scroll to bottom
    setTimeout(() => {
      chatHistoryRef.current?.scrollTo({
        top: chatHistoryRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }, 100);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  function enableFullScreen() {
    setChatbotOpenFullScreen((prev) => !prev);
  }

  function toggleChatbot() {
  //   const chatbotIcon = document.getElementById("chatbotIcon");
  //   const chatbotContainer = document.getElementById("chatbotContainer");

  //   chatbotIcon?.addEventListener('click', () => {
  //     chatbotContainer?.classList.toggle("active");
  // })
    setChatbotOpen((prev) => !prev);
  }
  
  return (
    <div className="min-h-screen bg-gray-50 bg-african-pattern relative">
      {location.pathname !== '/' && <Header />}
      {/* Remove wrapper div for landing page to avoid extra padding/margins */}
      {location.pathname === '/' ? (
        <Routes>
          <Route path="/" element={<LandingPage />} />
        </Routes>
      ) : (
        sidebarOpen ? (
          <div className="grid grid-cols-[320px_1fr] transition-all duration-300">
            {/* Sidebar */}
            <div className="bg-white shadow-lg">
              <Sidebar />
            </div>
            {/* Main Content */}
            <main className="overflow-hidden max-w-full px-4 sm:px-6 lg:px-8">
              <Routes>
                <Route path="/translation" element={<TranslationHub />} />
                <Route path="/stories" element={<StoryExplorer />} />
                <Route path="/games" element={<GameHub />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="/help" element={<div>Help Page</div>} />
                <Route path="*" element={<Navigate to="/translation" replace />} />
              </Routes>
            </main>
          </div>
        ) : (
          <main className="overflow-hidden max-w-full px-4 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/translation" element={<TranslationHub />} />
              <Route path="/stories" element={<StoryExplorer />} />
              <Route path="/games" element={<GameHub />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/help" element={<div>Help Page</div>} />
              <Route path="*" element={<Navigate to="/translation" replace />} />
            </Routes>
          </main>
        )
      )}
      {/* Chatbot FAB (Floating Action Button) */}
      <div className="fixed right-0 z-10 opacity-70 hover:opacity-100 bottom-10 md:right-[-25px] p-2 md:p-6 mt-12">
        <TbMessageChatbotFilled size={50} onClick={toggleChatbot} id='chatbotIcon' aria-label='Cultura Chatbot' title='Cultura Chatbot' className='cursor-pointer hover:scale-110 duration-200' />
      </div>
      {/* Chatbot Container - always visible */}
      <div
        id="chatbotContainer"
        className={`chatbot-container max-sm:p-0 max-sm:border max-sm:border-blue-600 fixed rounded-lg ${chatbotOpenFullScreen === true ? 'h-[90%] bottom-0 right-0 w-full mx-auto' : 'bottom-5 right-5 md:w-1/3 md:h-1/2 w-[90%]'} h-2/3 bg-white rounded-tl-xl shadow-2xl flex flex-col z-40 ${chatbotOpen ? 'block' : 'hidden'}`}
      >
        <div className="bg-blue-600 text-white p-4 rounded-tl-xl flex justify-between items-center">
          <div className="flex gap-2">
            <button id="closeChatbotFullScreen" className="text-white hover:text-gray-200 focus:outline-none" onClick={enableFullScreen} aria-label="Enable Fullscreen">
              {chatbotOpenFullScreen === false ? (
                <MdFullscreen title='Fullscreen' className='my-auto hover:scale-105 cursor-pointer' size={30} />
              ) : (
                <MdOutlineFullscreenExit title='Fullscreen' className='my-auto hover:scale-105 cursor-pointer' size={30} />
              )}
            </button>
            <h3 className="text-lg font-semibold">Cultura-ai Chatbot</h3>
          </div>
          <button
            id="closeChatbot"
            className="text-white hover:text-gray-200 focus:outline-none"
            onClick={toggleChatbot}
            aria-label="Close chatbot"
          >
            <div>
              <RxCross2 title='Close Chatbot' className='my-auto hover:scale-105 cursor-pointer' size={30} />
            </div>
          </button>
        </div>
        <div ref={chatHistoryRef} id="chatHistory" className="chat-history flex-grow p-4 overflow-y-auto space-y-4">
          {messages.map((msg, index) => (
            <div key={index} className={`flex mb-2 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`p-3 rounded-lg max-w-[80%] shadow-sm ${msg.sender === 'user' ? 'bg-blue-100 text-blue-800' : 'bg-gray-200 text-gray-800'}`}>
                {msg.text}
              </div>
            </div>
          ))}
        </div>
        <div className="p-4 border-t border-gray-200 flex items-center">
          <input type="text" id="chatInput" placeholder="Type your message..."
            className="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mr-3" value={inputValue} onChange={(e) => setInputValue(e.target.value)} onKeyPress={handleKeyPress} />
          <button id="sendMessage"
            className="px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-150 ease-in-out"
            onClick={handleSendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};