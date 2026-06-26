import { useState, useEffect } from 'react';
import api from '../services/api';
import { FiDownload, FiFileText } from 'react-icons/fi';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await api.get('/reports');
      setReports(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async () => {
    setGenerating(true);
    try {
      await api.get('/reports/csv');
      fetchReports();
      alert('Report generated successfully.');
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-500 flex justify-center items-center h-full">Loading reports...</div>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Reports</h2>
        <button 
          onClick={generateReport}
          disabled={generating}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors shadow-sm disabled:opacity-50"
        >
          <FiDownload /> {generating ? 'Generating...' : 'Generate New Report (CSV)'}
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-100">
              <th className="p-4 text-sm font-semibold text-gray-600">Title</th>
              <th className="p-4 text-sm font-semibold text-gray-600">Type</th>
              <th className="p-4 text-sm font-semibold text-gray-600">Date Generated</th>
              <th className="p-4 text-sm font-semibold text-gray-600 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {reports.length === 0 ? (
              <tr>
                <td colSpan="4" className="p-8 text-center text-gray-500">No reports generated yet.</td>
              </tr>
            ) : (
              reports.map(report => (
                <tr key={report.id} className="hover:bg-gray-50 transition-colors">
                  <td className="p-4 text-sm font-medium text-gray-800 flex items-center gap-2">
                    <FiFileText className="text-blue-500" /> {report.title}
                  </td>
                  <td className="p-4 text-sm text-gray-600">
                    <span className="bg-gray-100 px-2 py-1 rounded text-xs font-semibold shadow-sm">{report.type}</span>
                  </td>
                  <td className="p-4 text-sm text-gray-600">{new Date(report.created_at).toLocaleString()}</td>
                  <td className="p-4 text-right">
                    <button className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors">Download</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Reports;
