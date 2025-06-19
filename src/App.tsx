import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout/Layout';
import { motion } from 'framer-motion';

function App() {
  return (
    <Router>
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="App"
      >
        <Routes>
          <Route path="/" element={<Layout />} />
          <Route path="/*" element={<Layout />} />
        </Routes>
      </motion.div>
    </Router>
  );
}

export default App;