import React from 'react';

const Header = () => {
  return (
    <div hd-wrapper>
        <div className="hd-container flex justify-around items-center h-[80px] fixed w-[100vw] bg-[#342603] border-b-1 border-b-red-500 text-white">
            <div className='text-3xl font-bold'>CULTURAAI</div>
            <div className='hd-list list-none flex justify-around items-center space-x-8'>
                <span class="relative inline-block group">
                    <span class="relative z-10 hover:text-green-500">Home</span>
                    <span class="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span class="relative inline-block group">
                    <span class="relative z-10 hover:text-green-500">About</span>
                    <span class="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span class="relative inline-block group">
                    <span class="relative z-10 hover:text-green-500">Services</span>
                    <span class="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span class="relative inline-block group">
                    <span class="relative z-10 hover:text-green-500">How It Works</span>
                    <span class="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span class="relative inline-block group">
                    <span class="relative z-10 hover:text-green-500">News</span>
                    <span class="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span class="relative inline-block group">
                    <span class="relative z-10 hover:text-green-500">Blog</span>
                    <span class="absolute left-0 bottom-0 w-full h-0.5 bg-green-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-bottom duration-300"></span>
                </span>
                <span class="relative inline-block group p-2 border-2 border-green-500 rounded-md hover:bg-green-500 hover:text-white transition-colors duration-300">
                    <span class="relative z-10 font-semibold text-xl">CONTACT</span>
                </span>
            </div>

        </div>
    </div>
  )
}

export default Header
