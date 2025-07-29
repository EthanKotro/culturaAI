import React from 'react';

const SettingsPage: React.FC = () => {
  return (
    <div className="py-12 px-4 max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-primary-700">Settings</h2>
      <div className="bg-white rounded-xl shadow p-8 flex flex-col gap-6">
        <div>
          <h3 className="text-lg font-semibold mb-2">Account</h3>
          <div className="flex flex-col gap-2">
            <label className="text-gray-700">Name</label>
            <input className="border rounded-lg px-3 py-2" type="text" placeholder="Your Name" />
            <label className="text-gray-700 mt-4">Email</label>
            <input className="border rounded-lg px-3 py-2" type="email" placeholder="Your Email" />
          </div>
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-2">Preferences</h3>
          <div className="flex items-center gap-2">
            <input type="checkbox" id="darkmode" className="accent-primary-500" />
            <label htmlFor="darkmode" className="text-gray-700">Enable dark mode</label>
          </div>
        </div>
        <div>
          <button className="mt-6 px-6 py-3 bg-primary-500 text-white rounded-lg font-semibold hover:bg-primary-600 transition-colors">Save Changes</button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
