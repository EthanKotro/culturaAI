import React from 'react';

const HowItWorks = () => {
  return (
    <section id="how-it-works" className="hiw-wrapper">
      <div className="hiw-container border-b border-red-500 bg-[#342603]/90 p-2 md:p-6 flex flex-col text-white justify-start">
        <div className="flex flex-col p-3 md:p-12">
          <h1 className="text-green-500 font-semibold">EXPERIENCE AFRICAN CULTURE</h1>
          <h2 className="font-bold text-2xl md:text-4xl">Engage with heritage through innovative tools</h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full p-2 md:p-6">
            {[1, 2, 3, 4].map((_, i) => (
              <div
                key={i}
                className="card flex flex-col hover:bg-[#342603]/30 mt-10 h-[20rem] md:h-[25rem] rounded-md overflow-hidden"
              >
                <div className="h-[16rem] overflow-hidden">
                  <img
                    src={`https://picsum.photos/seed/hiw-${i}/600/400`}
                    alt="CulturaAi-HowItWorks"
                    className="w-full h-full object-cover"
                  />
                </div>
                <h3 className="text-lg md:text-2xl font-semibold my-2 ps-1 pt-3">
                  AI Voice Translator {i + 1}
                </h3>
                <p className="md:text-xl text-md mt-2 mb-4 ps-1">
                  Translate and narrate phrases into native African languages.
                </p>
                <span className="underline cursor-pointer p-1 w-fit ps-1 hover:text-green-400">
                  Learn more
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
