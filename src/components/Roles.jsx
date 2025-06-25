import React from 'react';
import { Brain, Server, Monitor, Palette, Link, Search } from 'lucide-react';

const Roles = () => {
  const teamMembers = [
    {
      name: "Ethan Kisang",
      role: "AI Lead",
      description: "Share your knowledge and passion for African culture.",
      icon: <Brain className="w-8 h-8" />,
    },
    {
      name: "Cecil Kioko",
      role: "Backend Developer",
      description: "Share your knowledge and passion for African culture.",
      icon: <Server className="w-8 h-8" />,
    },
    {
      name: "Emmanuel Mwangangi",
      role: "Frontend Developer",
      description: "Share your knowledge and passion for African culture.",
      icon: <Monitor className="w-8 h-8" />,
    },
    {
      name: "Philip Muendo",
      role: "UI/UX Designer",
      description: "Share your knowledge and passion for African culture.",
      icon: <Palette className="w-8 h-8" />,
    },
    {
      name: "Walter Simon",
      role: "Integrations",
      description: "Share your knowledge and passion for African culture.",
      icon: <Link className="w-8 h-8" />,
    },
    {
      name: "Erick Munyaka",
      role: "Researcher",
      description: "Share your knowledge and passion for African culture.",
      icon: <Search className="w-8 h-8" />,
    }
  ];

  return (
    <div className='roles-wrapper' id='team'>
    <section className="py-20 bg-[#342603]/90">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-green-500 text-xl font-semibold">Join the Movement</h2>
          <h1 className="text-white text-3xl md:text-5xl font-bold mt-2">
            Contribute to the future of African culture
          </h1>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {teamMembers.map((member, index) => (
            <div
              key={index}
              className="bg-[#2c1f05] hover:bg-[#3f2e08] rounded-xl p-6 shadow-md hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            >
              <div className="text-center">
                <div className="w-20 h-20 bg-[#4caf50]/30 rounded-full flex items-center justify-center mx-auto mb-4">
                  <div className="text-green-400">
                    {member.icon}
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white">{member.name}</h3>
                <p className="text-[#f5e9d2] font-semibold mt-1">{member.role}</p>
                <p className="text-[#e0d6c4] mt-3 text-sm leading-relaxed">
                  {member.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
    </div>
  );
};

export default Roles;
