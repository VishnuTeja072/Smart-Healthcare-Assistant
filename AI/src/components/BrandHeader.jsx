import React from 'react';

const BrandHeader = ({ size = 'medium', showTagline = false }) => {
  const sizes = {
    small: { img: 'w-8 h-8', title: 'text-lg' },
    medium: { img: 'w-10 h-10', title: 'text-2xl' },
    large: { img: 'w-12 h-12', title: 'text-4xl' }
  };

  const s = sizes[size] || sizes['medium'];

  return (
    <div className={`flex items-center gap-3`}>
      <img src="/logo.png" alt="logo" className={`${s.img} rounded-md object-cover`} />
      <div className="flex flex-col items-start leading-tight">
        <div className={`${s.title} font-serif italic text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 tracking-tighter`}>Smart Health Assistant</div>
        {showTagline && (
          <div className="text-[11px] font-bold text-gray-500 uppercase tracking-wider">AI healthcare assistant</div>
        )}
      </div>
    </div>
  );
};

export default BrandHeader;
