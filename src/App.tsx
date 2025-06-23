import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Layout } from './components/Layout/Layout'

function App() {
  const [count, setCount] = useState(0)

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
  )
}

export default App
