import React from 'react'

const About = () => {
  return (
    <div className='about-wrapper'>
      <div className="about-container border-b-1 border-b-red-500 bg-[#342603]/90 p-6 flex h-[calc(100vh-80px)] text-white justify-around items-center">
          <div className="flex flex-col w-[40%] space-y-2">
            <h1 className='text-green-500 font-semibold'>Embrace your heritage</h1>
            <h2 className='text-2xl font-bold'>Explore, learn, and connect</h2>
            <p className='text-wrap'>CulturaAi harnesses the power of artificial intelligence to celebrate and preserve the vibrant tapestry of African culture. With features like our AI Voice Translator, you can effortlessly translate and hear English phrases in native languages like Kikuyu, Swahili, Yoruba, and Zulu. Discover traditional African stories through our Cultural Story Narrator, engage with interactive games in our Game Hub, and share your own narratives on our Community Stories page. Join us in fostering a deeper understanding and appreciation of Africa's rich heritage.</p>
            <span className='underline'>Get in touch</span>
          </div>
          <div>
            <img src="https://picsum.photos/500/500?grayscale" alt="CulturaAi-About" />
          </div>
      </div>
    </div>
  )
}

export default About
