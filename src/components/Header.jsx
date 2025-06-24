import React, { useEffect, useState } from 'react';
import { IoMenuOutline } from 'react-icons/io5';

const sections = ['home', 'about', 'services', 'how-it-works', 'roles', 'contact'];

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('home');

  const toggleMenu = () => setMenuOpen(prev => !prev);

  // Lock scroll when mobile menu is open
  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : 'auto';
  }, [menuOpen]);

  // Track active section in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      { threshold: 0.5 }
    );

    sections.forEach(id => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const linkClass = id =>
    `relative z-10 hover:text-green-500 capitalize transition ${
      activeSection === id ? 'text-green-500 font-bold' : ''
    }`;

  return (
    <header className="hd-wrapper">
      <div className="hd-container flex justify-between max-sm:ps-6 md:justify-around items-center h-[80px] fixed w-full top-0 z-50 bg-[#342603] text-white border-b border-red-500">
        <div className="text-3xl font-bold">CULTURAAI</div>

        {/* Desktop Nav */}
        <nav className="hd-list list-none md:flex justify-around items-center space-x-8 hidden">
          {sections.map(id => (
            <span key={id} className="relative inline-block group">
              <a href={`#${id}`} className={linkClass(id)}>
                {id.replace('-', ' ')}
              </a>
              <span className="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
            </span>
          ))}
        </nav>

        {/* Hamburger Button */}
        <div className="md:hidden pe-4">
          <button onClick={toggleMenu} className="text-white text-3xl focus:outline-none">
            <IoMenuOutline size={35} />
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="hd-mobile-menu fixed inset-0 bg-[#342603]/95 flex flex-col items-center justify-center z-40 transition-all duration-300">
          <ul className="list-none space-y-6 text-white text-2xl text-center">
            {sections.map(id => (
              <li key={id}>
                <a
                  href={`#${id}`}
                  onClick={toggleMenu}
                  className={`${linkClass(id)} hover:text-green-400`}
                >
                  {id.replace('-', ' ')}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </header>
  );
};

export default Header;
