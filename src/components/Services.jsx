import React, { useState } from 'react';
import { Languages, BookOpen, Gamepad2 } from 'lucide-react';

const howItWorksItems = [
  {
    icon: <Languages className="w-12 h-12 text-[#FFD700]" />,
    title: "Translator",
    subtitle: "Speak and get translated instantly",
    description: "Translate and narrate phrases into native African languages using real-time AI voice tools.",
    features: ["Real-time audio", "Cultural context", "Multiple languages"]
  },
  {
    icon: <BookOpen className="w-12 h-12 text-[#FFD700]" />,
    title: "Folktale Explorer",
    subtitle: "Explore African cultural stories",
    description: "Dive into traditional tales from Kikuyu, Kamba, and Luo cultures with voice narration and context.",
    features: ["Narrated stories", "Cultural notes", "Multiple languages"]
  },
  {
    icon: <Gamepad2 className="w-12 h-12 text-[#FFD700]" />,
    title: "Language Games",
    subtitle: "Play and learn interactively",
    description: "Learn vocabulary and grammar through engaging language games designed for African dialects.",
    features: ["Fun challenges", "Track progress", "Share achievements"]
  }
];

const Services = () => {
  const [flippedIndex, setFlippedIndex] = useState(null);

  const handleFlip = (index) => {
    // Toggle flip state
    setFlippedIndex(flippedIndex === index ? null : index);
  };

  return (
    <section id="services" className="py-20 bg-gradient-to-b from-[#342603] to-[#1f1504]">
      <style>{`
        .perspective-1000 {
          perspective: 1000px;
        }
        .transform-style-preserve-3d {
          transform-style: preserve-3d;
        }
        .backface-hidden {
          backface-visibility: hidden;
        }
        .rotate-y-180 {
          transform: rotateY(180deg);
        }
      `}</style>

      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-green-500 font-semibold text-xl">EXPERIENCE AFRICAN CULTURE</h2>
          <h1 className="text-4xl md:text-5xl font-bold text-white mt-2">
            Engage with heritage through innovative tools
          </h1>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10 max-w-6xl mx-auto">
          {howItWorksItems.map((item, index) => (
            <div
              key={index}
              className="group perspective-1000 h-96 cursor-pointer"
              onClick={() => handleFlip(index)}
            >
              <div
                className={`relative w-full h-full transition-transform duration-700 transform-style-preserve-3d ${
                  flippedIndex === index ? 'rotate-y-180' : ''
                } group-hover:rotate-y-180`}
              >
                {/* Front of card */}
                <div className="absolute inset-0 w-full h-full backface-hidden bg-[#4B2E2E] rounded-2xl p-6 flex flex-col items-center justify-center text-center shadow-xl">
                  <div className="mb-4">
                    {item.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-[#FFD700] mb-2">{item.title}</h3>
                  <p className="text-[#D6B06F] text-lg">{item.subtitle}</p>
                  <p className="mt-6 text-[#F3EDE3] text-sm opacity-75">Tap or hover to learn more</p>
                </div>

                {/* Back of card */}
                <div className="absolute inset-0 w-full h-full backface-hidden rotate-y-180 bg-[#6B4C3B] rounded-2xl p-6 shadow-xl overflow-y-auto">
                  <h3 className="text-xl font-bold text-[#FFD700] mb-2">{item.title}</h3>
                  <p className="text-[#F3EDE3] mb-4 text-sm leading-relaxed">{item.description}</p>
                  <h4 className="text-[#D6B06F] font-semibold text-sm mb-2">Key Features:</h4>
                  <ul className="space-y-1">
                    {item.features.map((feature, i) => (
                      <li key={i} className="flex items-start text-sm text-[#F3EDE3]">
                        <span className="w-2 h-2 mt-1 bg-[#FFD700] rounded-full mr-3"></span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;
