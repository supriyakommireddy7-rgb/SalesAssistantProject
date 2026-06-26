import { useState, useEffect } from 'react';
import api from '../services/api';
import { FiRefreshCw, FiUser } from 'react-icons/fi';

const EmailInbox = () => {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [replyText, setReplyText] = useState('');

  useEffect(() => {
    fetchEmails();
  }, []);

  const fetchEmails = async () => {
    try {
      const res = await api.get('/emails');
      setEmails(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSync = async () => {
    setSyncing(true);
    try {
      await api.post('/emails/sync');
      fetchEmails();
    } catch (err) {
      console.error(err);
    } finally {
      setSyncing(false);
    }
  };

  const handleManualReply = async (e) => {
    e.preventDefault();
    if (!selectedEmail) return;
    try {
      await api.post(`/emails/${selectedEmail.id}/reply`, { reply_text: replyText });
      setReplyText('');
      setSelectedEmail(null);
      fetchEmails();
    } catch (err) {
      console.error(err);
      alert('Failed to send reply');
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-500">Loading inbox...</div>;

  return (
    <div className="p-6 max-w-7xl mx-auto flex h-[calc(100vh-4rem)]">
      <div className={`${selectedEmail ? 'w-1/2 hidden md:flex' : 'w-full flex'} flex-col bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mr-0 md:mr-6`}>
        <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50 shrink-0">
          <h2 className="text-xl font-bold text-gray-800">Email Inbox</h2>
          <button 
            onClick={handleSync} 
            disabled={syncing}
            className="flex items-center gap-2 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 shadow-sm"
          >
            <FiRefreshCw className={syncing ? "animate-spin" : ""} /> Sync Gmail
          </button>
        </div>
        <div className="overflow-y-auto flex-1">
          {emails.length === 0 ? (
            <div className="p-8 text-center text-gray-500">No emails found</div>
          ) : (
            <ul className="divide-y divide-gray-100">
              {emails.map(email => (
                <li 
                  key={email.id} 
                  onClick={() => setSelectedEmail(email)}
                  className={`p-4 cursor-pointer hover:bg-blue-50 transition-colors ${selectedEmail?.id === email.id ? 'bg-blue-50 border-l-4 border-blue-500' : 'border-l-4 border-transparent'}`}
                >
                  <div className="flex justify-between items-start mb-1">
                    <span className="font-semibold text-gray-800 truncate pr-2">{email.sender}</span>
                    <span className="text-xs text-gray-500 whitespace-nowrap shrink-0">{new Date(email.date).toLocaleDateString()}</span>
                  </div>
                  <h4 className="text-sm font-medium text-gray-700 truncate mb-3">{email.subject}</h4>
                  <div className="flex items-center gap-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      email.status === 'Unread' ? 'bg-red-100 text-red-700' :
                      email.status === 'Awaiting Human Response' ? 'bg-amber-100 text-amber-700' :
                      email.status === 'AI Replied' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'
                    }`}>
                      {email.status}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {selectedEmail && (
        <div className="w-full md:w-1/2 flex flex-col bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50 shrink-0">
            <h3 className="font-bold text-gray-800 truncate pr-4">{selectedEmail.subject}</h3>
            <button onClick={() => setSelectedEmail(null)} className="md:hidden text-gray-500 hover:text-gray-800 shrink-0">Close</button>
          </div>
          <div className="p-6 overflow-y-auto flex-1 border-b border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 shrink-0">
                <FiUser />
              </div>
              <div className="min-w-0">
                <p className="font-medium text-gray-800 truncate">{selectedEmail.sender}</p>
                <p className="text-xs text-gray-500">{new Date(selectedEmail.date).toLocaleString()}</p>
              </div>
            </div>
            <div className="text-gray-700 whitespace-pre-wrap font-sans text-sm bg-gray-50 p-5 rounded-lg border border-gray-100 shadow-inner">
              {selectedEmail.body}
            </div>
          </div>
          {selectedEmail.status === 'Awaiting Human Response' && (
            <div className="p-5 bg-gray-50 shrink-0">
              <h4 className="text-sm font-semibold text-gray-700 mb-3">Send Manual Reply</h4>
              <form onSubmit={handleManualReply}>
                <textarea
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none mb-3 text-sm shadow-sm"
                  rows="4"
                  placeholder="Type your reply here..."
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  required
                ></textarea>
                <div className="flex justify-end">
                  <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm">
                    Send Reply
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EmailInbox;
