import React from "react";

const AssessmentResult = ({ result, activeTab, latency }) => {
  if (!result) return null;

  return (
    <div className="mt-8 space-y-6 animate-in fade-in duration-500 w-full overflow-hidden">
      
      {/* Urgency Alert */}
      {(result.urgency === "High" || result.emergency) && (
        <div className="border border-red-200 bg-red-50/30 text-red-600 p-4 text-xs font-bold text-center tracking-widest uppercase rounded-lg break-words">
          ⚠️ Priority: Urgent Medical Attention Required
        </div>
      )}

      {/* Clinical Summary */}
      <section className="border-l-4 border-purple-400 pl-4 py-2 bg-purple-50/50 rounded-r-lg overflow-hidden">
        <h3 className="text-[10px] font-black text-purple-600 uppercase tracking-widest mb-1">
          Clinical Summary
        </h3>

        <p className="text-gray-800 text-sm sm:text-base leading-relaxed italic break-words">
          “{result.summary}”
        </p>

        {latency !== null && (
          <div className="mt-2 text-[9px] font-bold text-purple-500 uppercase tracking-tighter">
            Processed in {latency.toFixed(0)}ms {latency < 100 && "• (Cached)"}
          </div>
        )}
      </section>

      {/* Detail Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
        
        {/* Conditions */}
        <div className="border border-purple-200 bg-purple-50/30 p-4 rounded-lg overflow-hidden">
          <h4 className="text-[9px] font-black text-purple-600 uppercase tracking-widest mb-3">
            Conditions
          </h4>

          <div className="flex flex-wrap gap-1">
            {result.possible_conditions?.map((item, i) => (
              <span
                key={i}
                className="text-[10px] font-bold text-purple-700 bg-purple-100 px-2 py-0.5 rounded-sm break-words"
              >
                {item}
              </span>
            ))}
          </div>
        </div>

        {/* Specialist */}
        <div className="border border-pink-200 bg-pink-50/30 p-4 flex flex-col justify-center items-center rounded-lg text-center overflow-hidden">
          <h4 className="text-[9px] font-black text-pink-600 uppercase tracking-widest mb-1">
            Recommended
          </h4>
          <p className="text-base sm:text-lg font-black text-pink-700 tracking-tighter break-words">
            {result.specialist}
          </p>
        </div>
      </div>

      {/* Advice */}
      {result.advice && (
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 p-4 rounded-lg overflow-hidden">
          <h4 className="text-[9px] font-black text-purple-600 uppercase tracking-widest mb-2">
            Next Steps
          </h4>

          <ul className="space-y-1">
            {result.advice.map((a, i) => (
              <li
                key={i}
                className="text-xs sm:text-sm text-gray-600 flex gap-2 break-words"
              >
                <span className="text-purple-500 font-bold">•</span>
                <span className="break-words">{a}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default AssessmentResult;
