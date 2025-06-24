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
        <section id="home"><Home /></section>
        <section id="about"><About /></section>
        <section id="services"><Services /></section>
        <section id="how-it-works"><HowItWorks /></section>
        <section id="roles"><Roles /></section>
        <section id="contact"><Contact /></section>
        <br />
      </div>
    </>
  )
}

export default App
