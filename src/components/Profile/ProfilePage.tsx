import React from 'react';

const ProfilePage: React.FC = () => {
  return (
    <div className="py-12 px-4 max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-primary-700">Your Profile</h2>
      <div className="bg-white rounded-xl shadow p-8 flex flex-col gap-6">
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 rounded-full bg-secondary-200 flex items-center justify-center text-3xl font-bold text-secondary-700">
            {/* User avatar or initials */}
            <span>U</span>
          </div>
          <div>
            <div className="text-xl font-semibold text-gray-900">User Name</div>
            <div className="text-gray-500">user@email.com</div>
          </div>
        </div>
        <div className="flex gap-8 mt-4">
          <div>
            <div className="text-2xl font-bold text-primary-600">1200</div>
            <div className="text-gray-500 text-sm">Points</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-primary-600">5</div>
            <div className="text-gray-500 text-sm">Stories Shared</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-primary-600">3</div>
            <div className="text-gray-500 text-sm">Games Played</div>
          </div>
        </div>
        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-2">About</h3>
          <p className="text-gray-700">Welcome to your CulturaAI profile! Here you can track your progress, see your contributions, and manage your account.</p>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
