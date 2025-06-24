import React from 'react';

const Home = () => {
  return (
    <div id="home" className="home-wrapper">
      <div
        className="home-container relative flex flex-col justify-center md:items-start items-center h-[calc(100vh-80px)] text-white border-b border-red-500 p-4 pt-2 md:p-6 ps-10 md:ps-18 mt-4 md:mt-12"
        style={{
          backgroundImage: `url('https://storage.googleapis.com/workspace-0f70711f-8b4e-4d94-86f1-2a93ccde5887/image/18f8e75e-60cb-41a4-9037-ba65c31ef160.png')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          filter: 'brightness(1.1)'
        }}
      >
        {/* Overlay */}
        <div className="absolute inset-0 bg-[#342603]/85 z-0" />

        {/* Content */}
        <div className="relative z-10 flex flex-col w-[70%]">
          <h1 className="lg:text-8xl text-6xl font-bold leading-tight">
            Embrace African Heritage
          </h1>
          <p className="text-2xl mt-4">Discover the richness of culture</p>
          <button className="mt-6 p-2 px-4 rounded-sm bg-green-500 hover:bg-green-500/80 w-fit">
            VIEW SERVICES
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
