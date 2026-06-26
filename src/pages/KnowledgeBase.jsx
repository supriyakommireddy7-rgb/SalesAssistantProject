import { useState, useEffect } from 'react';
import api from '../services/api';
import { FiPlus, FiEdit2, FiTrash2 } from 'react-icons/fi';

const KnowledgeBase = () => {
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFaqs();
  }, []);

  const fetchFaqs = async () => {
    try {
      const res = await api.get('/knowledge_base');
      setFaqs(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteFaq = async (id) => {
    if (window.confirm('Delete this FAQ?')) {
      try {
        await api.delete(`/knowledge_base/${id}`);
        fetchFaqs();
      } catch (err) {
        console.error(err);
      }
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-500 flex justify-center items-center h-full">Loading Knowledge Base...</div>;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Knowledge Base (FAQs)</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors shadow-sm">
          <FiPlus /> Add FAQ
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          {faqs.map(faq => (
            <div key={faq.id} className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-lg text-gray-800 pr-4">{faq.question}</h3>
                <div className="flex gap-2 shrink-0">
                  <button className="text-blue-600 hover:bg-blue-50 p-1.5 rounded-lg transition-colors"><FiEdit2 size={16} /></button>
                  <button onClick={() => deleteFaq(faq.id)} className="text-red-600 hover:bg-red-50 p-1.5 rounded-lg transition-colors"><FiTrash2 size={16} /></button>
                </div>
              </div>
              <p className="text-gray-600 text-sm whitespace-pre-wrap mb-4 bg-gray-50 p-3 rounded-lg border border-gray-100">{faq.answer}</p>
              <div className="flex flex-wrap gap-2 items-center text-xs">
                <span className="bg-white border border-gray-200 text-gray-600 px-2 py-1 rounded shadow-sm">Category: {faq.category}</span>
                <span className="bg-white border border-gray-200 text-gray-600 px-2 py-1 rounded shadow-sm truncate max-w-[250px]">Keywords: {faq.keywords}</span>
                <span className={`px-2 py-1 rounded font-medium shadow-sm ${faq.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                  {faq.status}
                </span>
              </div>
            </div>
          ))}
        </div>
        <div>
          <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 sticky top-24">
            <h3 className="font-semibold text-gray-800 mb-4">Rule-Based Fallback</h3>
            <p className="text-sm text-gray-600 mb-4">
              These FAQs are used by the Rule Engine if the Gemini AI API fails, returns low confidence, or is unavailable.
            </p>
            <div className="bg-blue-50 border border-blue-100 text-blue-800 text-sm p-4 rounded-lg shadow-inner">
              <span className="font-semibold">Tip:</span> Ensure keywords are comma-separated and accurately reflect potential customer queries.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeBase;
