



import React from 'react';

const HospitalCard = ({ hospital }) => {
  return (
    <div className="py-4 px-4 border border-purple-200 rounded-lg mb-2 flex justify-between items-center group hover:border-purple-300 transition-all bg-gradient-to-r from-purple-50 to-pink-50 shadow-md">
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <p className="font-bold text-sm text-gray-900 truncate uppercase tracking-tight">
            {hospital.name}
          </p>
          {hospital.rating > 0 && (
            <div className="flex items-center text-[10px] font-bold text-orange-500">
              <span>★</span>
              <span>{hospital.rating}</span>
            </div>
          )}
        </div>
        
        <p className="text-[11px] text-gray-500 truncate tracking-tight mb-2">
          {hospital.address}
        </p>

        <div className="flex items-center gap-3">
          {/* DISTANCE BADGE */}
          <span className="text-[10px] font-black text-purple-600 bg-purple-100 px-2 py-0.5 rounded uppercase">
            {hospital.distance_km > 0 ? `${hospital.distance_km} KM` : "NEARBY"}
          </span>
          
          {/* SPECIALIST TAG */}
          <span className="text-[9px] font-bold text-pink-600 uppercase tracking-widest">
            {hospital.available_specialist}
          </span>
        </div>
      </div>

      {/* DIRECTIONS BUTTON */}
      <a 
        href={hospital.maps_url} 
        target="_blank" 
        rel="noreferrer" 
        className="ml-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 text-[10px] font-black uppercase hover:from-purple-600 hover:to-pink-600 transition-all rounded-lg shadow-lg active:scale-95 whitespace-nowrap"
      >
        Get Directions
      </a>
    </div>
  );
};

export default HospitalCard;