

import BrandHeader from './BrandHeader';

const Navbar = ({ user, onLogout }) => (
  <nav className="flex justify-between items-center px-8 py-5 bg-white/90 backdrop-blur-sm border-b border-purple-200 sticky top-0 z-50 shadow-lg">
    <div className="flex items-center gap-3">
      <BrandHeader size="small" />
    </div>
    <div className="flex items-center gap-6">
      <div className="text-right">
        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-none">Logged in as</p>
        <p className="text-sm font-black text-gray-800">@{user}</p>
      </div>
      <button 
        onClick={onLogout}
        className="px-4 py-2 bg-gradient-to-r from-red-400 to-pink-400 hover:from-red-500 hover:to-pink-500 text-white rounded-xl text-[10px] font-black uppercase transition-all shadow-md"
      >
        Logout
      </button>
    </div>
  </nav>
);

export default Navbar;