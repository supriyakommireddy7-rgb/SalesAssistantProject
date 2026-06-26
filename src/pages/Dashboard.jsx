import { useState, useEffect } from 'react';
import api from '../services/api';
import { FiUsers, FiMail, FiMessageSquare, FiAlertCircle } from 'react-icons/fi';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get('/dashboard/stats');
      setStats(res.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-500 flex justify-center items-center h-full">Loading dashboard...</div>;
  if (!stats) return null;

  const chartData = [
    { name: 'AI Replies', count: stats.ai_replies, fill: '#3b82f6' },
    { name: 'Rule Based', count: stats.rule_replies, fill: '#10b981' },
    { name: 'Human Pending', count: stats.human_pending, fill: '#f59e0b' }
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Dashboard Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Customers" value={stats.total_customers} icon={<FiUsers />} color="bg-blue-500" />
        <StatCard title="Total Emails" value={stats.total_emails} icon={<FiMail />} color="bg-indigo-500" />
        <StatCard title="AI Handled" value={stats.ai_replies + stats.rule_replies} icon={<FiMessageSquare />} color="bg-green-500" />
        <StatCard title="Human Pending" value={stats.human_pending} icon={<FiAlertCircle />} color="bg-amber-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Reply Breakdown</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#6b7280'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#6b7280'}} />
                <Tooltip cursor={{fill: '#f3f4f6'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Notifications</h3>
          <div className="space-y-4">
            {stats.notifications.length === 0 ? (
              <p className="text-gray-500 text-sm">No new notifications</p>
            ) : (
              stats.notifications.map(notif => (
                <div key={notif.id} className="flex gap-3 items-start border-b border-gray-50 pb-3 last:border-0 last:pb-0">
                  <div className={`mt-1.5 flex-shrink-0 w-2.5 h-2.5 rounded-full ${notif.type === 'Warning' ? 'bg-amber-500' : 'bg-blue-500'}`}></div>
                  <div>
                    <p className="text-sm font-medium text-gray-800">{notif.title}</p>
                    <p className="text-xs text-gray-500 mt-1">{notif.message}</p>
                    <p className="text-xs text-gray-400 mt-1">{new Date(notif.created_at).toLocaleDateString()}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ title, value, icon, color }) => (
  <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center gap-5 hover:shadow-md transition-shadow">
    <div className={`w-14 h-14 rounded-xl flex items-center justify-center text-white text-2xl ${color} shadow-sm`}>
      {icon}
    </div>
    <div>
      <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
      <h4 className="text-2xl font-bold text-gray-800">{value}</h4>
    </div>
  </div>
);

export default Dashboard;
