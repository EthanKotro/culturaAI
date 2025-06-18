import React from 'react'

const Services = () => {
  return (
    <div className='services-wrapper'>
      <div className="services-container border-b-1 border-b-red-500 bg-[#342603]/90 p-6 flex flex-col h-[calc(100vh-80px)] text-white justify-start">
          <div className="flex flex-col p-12">
            <h1 className='text-green-500 font-semibold'>Embrace your heritage</h1>
            <h2 className='font-bold text-4xl'>Explore, learn, and share african culture</h2>
            <div className="flex w-screen justify-start space-x-9">
              <div className="card flex flex-col bg-[#342603]/70 mt-10 h-[13rem] w-[20rem]">
                <img src="" alt="" />
                <h1>AI voice translator </h1>
                <p>Translate and narate phrases into native African languages.</p>
              </div>
              <div className="card flex flex-col bg-[#342603]/70 mt-10 h-[13rem] w-[20rem]">
                <img src="" alt="" />
                <h1>AI voice translator </h1>
                <p>Translate and narate phrases into native African languages.</p>
              </div>
              <div className="card flex flex-col bg-[#342603]/70 mt-10 h-[13rem] w-[20rem]">
                <img src="" alt="" />
                <h1>AI voice translator </h1>
                <p>Translate and narate phrases into native African languages.</p>
              </div>
            </div>
          </div>
      </div>
    </div>
  )
}

export default Services
