import { useNavigate } from 'react-router-dom';
import { FiUser, FiLogOut } from 'react-icons/fi';

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('admin');
    navigate('/login');
  };

  return (
    <header className="bg-white shadow-sm h-16 flex items-center justify-between px-6 border-b border-gray-200 sticky top-0 z-10">
      <h1 className="text-xl font-semibold text-gray-800">Sales Dashboard</h1>
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/profile')} className="p-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors focus:outline-none">
          <FiUser size={20} />
        </button>
        <button onClick={handleLogout} className="p-2 text-red-600 hover:bg-red-50 rounded-full transition-colors focus:outline-none">
          <FiLogOut size={20} />
        </button>
      </div>
    </header>
  );
};

export default Header;
