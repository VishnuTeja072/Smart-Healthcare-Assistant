

import { useState } from "react";
import axios from "axios";
import AuthPage from "./components/AuthPage";
import Navbar from "./components/Navbar";
import TriageForm from "./components/TriageForm";
import AssessmentResult from "./components/AssessmentResult";
import HospitalCard from "./components/HospitalCard";
import MapView from "./components/MapView";
import BrandHeader from "./components/BrandHeader";

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL ? `${import.meta.env.VITE_BACKEND_URL}/api` : "http://127.0.0.1:8000/api";

const App = () => {
const [user, setUser] = useState(localStorage.getItem("username") || null);
const [activeTab, setActiveTab] = useState("health");
const [symptoms, setSymptoms] = useState("");
const [result, setResult] = useState(null);
const [hospitals, setHospitals] = useState([]);
const [loading, setLoading] = useState(false);
const [searchLoading, setSearchLoading] = useState(false);
const [error, setError] = useState("");
const [showHospitals, setShowHospitals] = useState(false); // Controls map visibility
const [latency, setLatency] = useState(null);
const [userLocation, setUserLocation] = useState(null);

  const formatLatency = (ms) => {
    if (!ms) return "";
    if (ms < 1000) return `${Math.round(ms)}ms`;
    return `${((ms / 1000).toFixed(2))}s`;
  };

  const switchTab = (tab) => {
    setActiveTab(tab);
    setResult(null);
    setHospitals([]);
    setSymptoms("");
    setError("");
    setShowHospitals(false);
    setLatency(null);
  };

  /**
   * FINAL GPS FIX:
   * Uses enableHighAccuracy to force the device to use GPS chips instead of ISP IP hubs.
   * Increased timeout to 12 seconds to ensure a lock in regional areas like Kuppam.
   */
const getCoordinates = () => {
    return new Promise((resolve) => {
      if (!navigator.geolocation) {
        resolve({ lat: 0, lon: 0 });
        return;
      }
      
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          console.log("GPS Lock:", pos.coords.latitude, pos.coords.longitude);
          resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude });
        },
        (err) => {
          console.error("GPS Error:", err.message);
          resolve({ lat: 0, lon: 0 }); 
        },
        { 
          enableHighAccuracy: true, 
          timeout: 10000, 
          maximumAge: 0 // DO NOT use cached location
        }
      );
    });
  };

const getAiAssessment = async () => {
  if (!symptoms.trim()) return setError("Please describe symptoms.");

  setLoading(true);
  setError("");
  setResult(null);
  setShowHospitals(false);

    const coords = await getCoordinates();
    setUserLocation(coords);
    const path = activeTab === "mental" ? "/mental-health/analyze" : "/hospitals/nearby";
    const fullUrl = `${API_BASE_URL}${path}`;

  // 1. GET THE TOKEN FROM STORAGE
  const token = localStorage.getItem("token");

  try {
    const response = await axios.post(fullUrl, {
      latitude: coords.lat,
      longitude: coords.lon,
      symptoms: symptoms
    }, { 
      timeout: 40000,
      // 2. ATTACH TOKEN TO HEADERS
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    setResult(response.data.triage);
    setHospitals(response.data.hospitals || []);
    setLatency(response.data.latency_ms);
  } catch (err) {
    console.error("Connection Error:", err);
    // 3. HANDLE EXPIRED TOKEN
    if (err.response?.status === 401) {
      setError("Session expired. Please log in again.");
      setTimeout(() => setUser(null), 2000); // Logout after 2 seconds
    } else {
      setError("AI Engine Unavailable. Verify backend is running.");
    }
  } finally {
    setLoading(false);
  }
};
  const locateSpecialist = () => {
    setSearchLoading(true);
    // Slight delay to simulate scanning and give smooth UX
    setTimeout(() => {
      setShowHospitals(true);
      setSearchLoading(false);
      // Smooth scroll to results
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }, 800);
  };

  if (!user) return <AuthPage onLoginSuccess={(username) => setUser(username)} />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-red-50 font-sans selection:bg-purple-100">
      <Navbar 
  user={user} 
  onLogout={() => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setUser(null);
  }} 
/>
      
      <main className="py-10 px-4 flex justify-center">
        <div className="w-full max-w-[600px] bg-white/90 backdrop-blur-sm border border-white/20 rounded-2xl p-8 shadow-2xl">
          <header className="text-center mb-8 flex items-center justify-center gap-3">
            <BrandHeader size="large" />
          </header>

          <nav className="flex border-b border-purple-200 mb-8">
            <button 
              onClick={() => switchTab("health")} 
              className={`flex-1 py-3 text-[10px] font-black uppercase tracking-[0.2em] transition-all ${activeTab === "health" ? "border-b-2 border-purple-600 text-purple-600" : "text-gray-400 hover:text-purple-400"}`}
            >
              Physical Health
            </button>
            <button 
              onClick={() => switchTab("mental")} 
              className={`flex-1 py-3 text-[10px] font-black uppercase tracking-[0.2em] transition-all ${activeTab === "mental" ? "border-b-2 border-purple-600 text-purple-600" : "text-gray-400 hover:text-purple-400"}`}
            >
              Mental Wellness
            </button>
          </nav>

          <TriageForm 
            symptoms={symptoms} 
            setSymptoms={setSymptoms} 
            activeTab={activeTab} 
            loading={loading} 
            onAnalyze={getAiAssessment} 
          />

          {error && (
            <div className="mt-4 text-red-500 text-[10px] font-bold uppercase text-center animate-bounce">
              {error}
            </div>
          )}

          {result && (
            <div className="animate-in fade-in slide-in-from-top-4 duration-700">
              <div className="relative">
                <AssessmentResult result={result} activeTab={activeTab} latency={latency} />
                {latency && (
                  <div className="absolute top-2 right-2 flex items-center gap-1.5">
                    <span className={`w-1.5 h-1.5 rounded-full ${latency < 500 ? 'bg-green-500 animate-pulse' : 'bg-blue-400'}`}></span>
                    <span className="text-[9px] font-black text-gray-400 uppercase tracking-widest">
                      {latency < 500 ? 'Cached' : 'Generated'} in {formatLatency(latency)}
                    </span>
                  </div>
                )}
              </div>
              
              <div className="mt-10 pt-8 border-t border-gray-100">
                {!showHospitals ? (
                  <button 
                    onClick={locateSpecialist} 
                    disabled={searchLoading} 
                    className="w-full bg-black text-white py-4 rounded-sm font-black text-[11px] uppercase tracking-[0.2em] hover:bg-gray-800 transition-all active:scale-95 shadow-lg"
                  >
                    {searchLoading ? "Verifying Facilities..." : `Find Nearby ${result.specialist}s`}
                  </button>
                ) : (
                  <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <div className="flex items-center justify-between px-1">
                      <p className="text-[9px] font-black uppercase text-gray-400 tracking-[0.2em]">Verified Recommendations</p>
                      <button 
                        onClick={() => setShowHospitals(false)}
                        className="text-[9px] font-bold text-blue-500 uppercase hover:underline"
                      >
                        Hide Maps
                      </button>
                    </div>

                    {/* Map View (OpenStreetMap + Leaflet) */}
                    <MapView hospitals={hospitals} userLocation={userLocation} />

                    <div className="space-y-2">
                      {hospitals.length > 0 ? (
                        hospitals.map((h, i) => (
                          <HospitalCard key={i} hospital={h} />
                        ))
                      ) : (
                        <p className="text-center text-gray-400 text-xs py-4">No facilities found within 15km.</p>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;