import { useState, useEffect } from 'react';
import api from '../services/api';
import { FiMessageSquare, FiUser, FiCpu } from 'react-icons/fi';

const ConversationHistory = () => {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await api.get('/conversations');
      setConversations(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-500 flex justify-center items-center h-full">Loading history...</div>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Conversation History</h2>
      
      <div className="space-y-6">
        {conversations.length === 0 ? (
          <div className="bg-white p-8 rounded-xl shadow-sm text-center text-gray-500 border border-gray-100">
            No conversations recorded yet.
          </div>
        ) : (
          conversations.map(conv => (
            <div key={conv.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="p-4 bg-gray-50 border-b border-gray-100 flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold shadow-sm ${
                    conv.reply_type === 'AI' ? 'bg-blue-100 text-blue-700' :
                    conv.reply_type === 'Rule-Based' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
                  }`}>
                    {conv.reply_type} Reply
                  </span>
                  {conv.confidence_score && (
                    <span className="text-xs text-gray-500 bg-white border border-gray-200 px-2 py-1 rounded-full shadow-sm">
                      Confidence: {(conv.confidence_score * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
                <span className="text-sm text-gray-500">{new Date(conv.date).toLocaleString()}</span>
              </div>
              <div className="p-5 flex gap-4 items-start">
                <div className="w-10 h-10 rounded-full flex items-center justify-center shrink-0 bg-blue-100 text-blue-600 shadow-inner">
                  {conv.reply_type === 'AI' ? <FiCpu size={20} /> : <FiUser size={20} />}
                </div>
                <div className="bg-gray-50 border border-gray-100 p-4 rounded-lg rounded-tl-none w-full shadow-sm text-sm text-gray-700 font-sans whitespace-pre-wrap">
                  {conv.reply_text}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ConversationHistory;
