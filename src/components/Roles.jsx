import React from 'react';

const Roles = () => {
  return (
    <section id="roles" className="rl-wrapper">
      <div className="rl-container border-b border-red-500 bg-[#342603]/90 p-4 md:p-6">
        <div className="flex flex-col p-6 md:p-12">
          <h1 className="text-green-500 font-semibold">Join the movement</h1>
          <h2 className="font-bold text-2xl md:text-4xl text-white">
            Contribute to the future of African culture
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 w-full p-2 md:p-6 gap-6">
            {[
              ['Ethan Kisang', 'AI Lead'],
              ['Cecil Kioko', 'Backend Dev'],
              ['Emmanuel Mwangangi', 'Frontend Dev'],
              ['Philip Muendo', 'UX Designer'],
              ['Walter Simon', 'Integrations'],
              ['Erick Munyaka', 'Researcher'],
            ].map(([name, title], i) => (
              <div
                key={i}
                className="card flex flex-col items-center hover:bg-[#342603]/70 mt-10 rounded-sm hover:scale-110 transition duration-300 p-4"
              >
                <div className="w-32 h-32 rounded-full overflow-hidden mb-3">
                  <img
                    src={`https://picsum.photos/seed/${i}/200`}
                    alt={name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <h1 className="text-lg md:text-xl font-semibold italianno-regular text-center">{name}</h1>
                <h2 className="text-xl md:text-2xl font-semibold underline text-center">{title}</h2>
                <p className="text-md md:text-lg mt-2 text-center">
                  Share your knowledge and passion for African culture.
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Roles;
