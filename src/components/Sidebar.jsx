import { Link, useLocation } from 'react-router-dom';
import { FiHome, FiUsers, FiMail, FiMessageSquare, FiBook, FiPieChart } from 'react-icons/fi';

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: <FiHome size={20} /> },
    { name: 'Customers', path: '/customers', icon: <FiUsers size={20} /> },
    { name: 'Email Inbox', path: '/inbox', icon: <FiMail size={20} /> },
    { name: 'Conversations', path: '/history', icon: <FiMessageSquare size={20} /> },
    { name: 'Knowledge Base', path: '/kb', icon: <FiBook size={20} /> },
    { name: 'Reports', path: '/reports', icon: <FiPieChart size={20} /> },
  ];

  return (
    <div className="w-64 bg-slate-900 text-white flex flex-col h-screen fixed top-0 left-0 shadow-xl">
      <div className="h-16 flex items-center justify-center border-b border-slate-800">
        <h2 className="text-lg font-bold tracking-wide text-blue-400 flex items-center gap-2">
          <FiMail className="text-blue-500" /> AI Sales Assistant
        </h2>
      </div>
      <nav className="flex-1 overflow-y-auto py-6">
        <ul className="space-y-2 px-4">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
            return (
              <li key={item.name}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                    isActive 
                      ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20' 
                      : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  {item.icon}
                  <span className="font-medium">{item.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
