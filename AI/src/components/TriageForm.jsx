

import React from 'react';

const TriageForm = ({ symptoms, setSymptoms, activeTab, loading, onAnalyze }) => {
  return (
    <div className="space-y-6">
      <textarea
        className="w-full border-2 border-gray-100 rounded-[2rem] p-6 focus:ring-8 focus:ring-blue-50 outline-none transition-all resize-none text-gray-700 font-medium leading-relaxed bg-gray-50/50 focus:bg-white"
        placeholder={activeTab === "mental" ? "Describe your emotional well-being..." : "Describe symptoms (e.g., sharp abdominal pain, bloating)..."}
        rows={5}
        value={symptoms}
        onChange={(e) => setSymptoms(e.target.value)}
      />

      <button
        onClick={onAnalyze}
        disabled={loading || !symptoms.trim()}
        className="w-full py-5 rounded-2xl font-black text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 shadow-xl disabled:bg-gray-300 transition-all active:scale-95 uppercase tracking-wider"
      >
        {loading ? "Processing AI Triage..." : "Get AI Assessment"}
      </button>
    </div>
  );
};

export default TriageForm;