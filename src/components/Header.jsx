import React, { useEffect, useRef, useState } from 'react';

const Header = () => {

    // const [activeSection, setActiveSection] = useState("home");

    // const sections = ["home", "about", "services", "how-it-works", "news", "blog", "contact"];

    // const sectionRefs = {
    //     home: useRef(null),
    //     about: useRef(null),
    //     services: useRef(null),
    //     howItWorks: useRef(null),
    //     contact: useRef(null)
    // };

    // useEffect(() => {
    //     const obserever = new IntersectionObserver(
    //         (entries) => {
    //             entries.forEach((entry) => {
    //                 if (entry.isIntersecting) {
    //                     setActiveSection(entry.target.id);
    //                 }
    //             });
    //         },
    //         {
    //             threshold: 0.5,
    //         }
    //     );

    //     sectionRefs.forEach((section) => {
    //         if (sectionRefs[section].current) {
    //             obserever.observe(sectionRefs[section].current);
    //         }
    //     });

    //     return () => obserever.disconnect();
    // }, []);

  return (
    <div className='hd-wrapper'>
        <div className="hd-container flex justify-around items-center h-[80px] fixed w-[100vw] bg-[#342603] border-b-1 border-b-red-500 text-white">
            <div className='text-3xl font-bold'>CULTURA AI</div>
            <div className='hd-list list-none flex justify-around items-center space-x-8'>
                <span className="relative inline-block group">
                    <a href='#home' className='active relative z-10 hover:text-green-500'>Home</a>
                    <span className="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span className="relative inline-block group">
                    <a href='#about' className='relative z-10 hover:text-green-500'>About</a>
                    <span className="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span className="relative inline-block group">
                    <a href='#services' className='relative z-10 hover:text-green-500'>Services</a>
                    <span className="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span className="relative inline-block group">
                    <a href='#how-it-works' className='relative z-10 hover:text-green-500'>How It Works</a>
                    <span className="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span className="relative inline-block group">
                    <a href='#news' className='relative z-10 hover:text-green-500'>News</a>
                    <span className="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span className="relative inline-block group">
                    <a href='#blog' className='relative z-10 hover:text-green-500'>Blog</a>
                    <span className="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span className="relative inline-block group p-2 border-2 border-green-500 rounded-md hover:bg-green-500 hover:text-white transition-colors duration-300">
                    <a href='#contact' className="relative z-10 font-semibold text-xl">CONTACT</a>
                </span>
            </div>

        </div>
    </div>
  )
}

export default Header
