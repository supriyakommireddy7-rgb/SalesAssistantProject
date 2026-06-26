import { useState, useEffect } from 'react';
import api from '../services/api';
import { FiUser } from 'react-icons/fi';

const Profile = () => {
  const [admin, setAdmin] = useState(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await api.get('/auth/profile');
      setAdmin(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (!admin) return <div className="p-8 text-center text-gray-500 flex justify-center items-center h-full">Loading profile...</div>;

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Admin Profile</h2>
      
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
        <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mx-auto mb-4 text-4xl shadow-inner">
          <FiUser />
        </div>
        <h3 className="text-xl font-bold text-gray-800 mb-1">@{admin.username}</h3>
        <p className="text-sm text-gray-500 mb-6 font-medium">Administrator</p>
        
        <div className="border-t border-gray-100 pt-6 mt-6">
          <div className="flex justify-between items-center max-w-sm mx-auto text-sm">
            <span className="text-gray-500">Account Created:</span>
            <span className="font-medium text-gray-800">{new Date(admin.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
