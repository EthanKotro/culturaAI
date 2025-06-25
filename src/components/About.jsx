import React from 'react';
import { Globe, Heart, Users } from 'lucide-react';

const About = () => {
  return (
    <section id="about" className="py-20 bg-[#342603]/90 text-white">
      <div className="container mx-auto px-6">
        
        {/* Description */}
        <div className="max-w-4xl mx-auto text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-green-500 mb-4">
            Embrace Your Heritage
          </h2>
          <p className="text-lg md:text-xl text-[#F3EDE3]/90 leading-relaxed font-serif">
            CulturaAI uses the power of artificial intelligence to celebrate and preserve Africa's vibrant culture.
            Explore various African languages,while engaging with traditional stories, games, and a community that reconnects you to your roots.
          </p>
        </div>

        {/* Icons */}
        <div className="grid md:grid-cols-3 gap-10 max-w-5xl mx-auto mb-20">
          {[{
            icon: Globe,
            title: 'Global Access',
            desc: 'Access African language tools from anywhere in the world.'
          }, {
            icon: Heart,
            title: 'Cultural Love',
            desc: 'Celebrate and preserve your cultural heritage with passion.'
          }, {
            icon: Users,
            title: 'Community',
            desc: 'Bridge generations and foster shared language experiences.'
          }].map(({ icon: Icon, title, desc }, idx) => (
            <div key={idx} className="flex flex-col items-center text-center px-4">
              <Icon className="w-16 h-16 text-[#D6B06F] mb-4" />
              <h3 className="text-xl font-semibold text-[#FFD700] mb-2">{title}</h3>
              <p className="text-[#F3EDE3]/80 text-base">{desc}</p>
            </div>
          ))}
        </div>

        {/* Explore, Learn, Connect */}
        <div className="text-center max-w-3xl mx-auto">
          <h3 className="text-2xl md:text-3xl font-bold mb-4 text-green-500">
            Explore, Learn, and Connect
          </h3>
          <p className="text-lg md:text-xl text-[#F3EDE3]/90 leading-relaxed font-serif">
            With CulturaAI, you’re not just learning a language — you're immersing yourself in traditions,
            stories, and voices that have shaped generations. Let technology reconnect us with heritage.
          </p>
        </div>
      </div>
    </section>
  );
};

export default About;
