import './App.css'
import About from './components/About'
import Contact from './components/Contact'
import Header from './components/Header'
import Home from './components/Home'
import HowItWorks from './components/HowItWorks'
import Roles from './components/Roles'
import Services from './components/Services'

function App() {
  return (
    <>
      <Header />
      <div className="w-[100vw] overflow-x-hidden">
        <Home />
        <About />
        <Services />
        <HowItWorks />
        <Roles />
        <Contact />
      </div>
    </>
  )
}

export default App
