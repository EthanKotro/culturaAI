import React from 'react'

const Home = () => {
  return (
    <div className='home-wrapper' id='home'>
      <div className="home-container border-b-1 border-b-red-500 bg-[#342603]/90 justify-center items-start p-6 ps-18 flex flex-col h-[calc(100vh-80px)] text-white">
          <div className="flex flex-col w-[70%]">
            <h1 className='text-8xl text-wrap font-bold'>Embrace african heritage</h1>
            <p className='text-2xl p-4 ps-0'>Discover the richness of culture</p>
          </div>
            <button className='p-2 px-4 rounded-sm cursor-pointer bg-green-500 hover:bg-green-500/80'>VIEW SERVICES</button>
      </div>
  </div>
  )
}

export default Home