import React from 'react'

const Services = () => {
  return (
    <div className='services-wrapper' id='services'>
      <div className="services-container border-b-1 border-b-red-500 bg-[#342603]/90 p-6 flex md:h-[100vh] flex-col text-white justify-start">
          <div className="flex flex-col p-6 md:p-12">
            <h1 className='text-green-500 font-semibold'>Embrace your heritage</h1>
            <h2 className='font-bold md:text-4xl text-2xl'>Explore, learn, and share african culture</h2>
            <div className="md:grid md:grid-cols-[1fr_1fr_1fr] flex flex-col w-[100%] justify-start p-6 space-x-4 md:gap-4">
              <div className="card flex flex-col bg-[#342603]/70 mt-10 h-[100%]">
                <img src="https://picsum.photos/400/200" alt="CulturaAi-About" />
                <h1 className='md:text-2xl text-xl font-semibold my-2 p-1'>AI voice translator </h1>
                <p className='md:text-lg text-md mt-2 mb-4 ms-1'>Translate and narate phrases into native African languages.</p>
              </div>
              <div className="card flex flex-col bg-[#342603]/70 mt-10 h-[100%]">
                <img src="https://picsum.photos/400/200" alt="CulturaAi-About" />
                <h1 className='text-2xl font-semibold my-2 p-1'>Game Hub</h1>
                <p className='text-lg mt-2 mb-4 ms-1'>Translate and narate phrases into native African languages.</p>
              </div>
              <div className="card flex flex-col bg-[#342603]/70 mt-10 h-[100%]">
                <img src="https://picsum.photos/400/200" alt="CulturaAi-About" />
                <h1 className='text-2xl font-semibold my-2 p-1'>Story Narrator</h1>
                <p className='text-lg mt-2 mb-4 ms-1'>Translate and narate phrases into native African languages.</p>
              </div>
              {/* <div className="card flex flex-col bg-[#342603]/70 mt-10 h-[13rem] w-[20rem]">
                <img src="" alt="" />
                <h1>AI voice translator </h1>
                <p>Translate and narate phrases into native African languages.</p>
              </div> */}
            </div>
          </div>
      </div>
    </div>
  )
}

export default Services
