"use client";

import { useState, useEffect } from "react";

export default function AttendancePage() {
  const [active, setActive] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const toggleAttendance = async (status: boolean) => {
    try {
      const res = await fetch(`http://localhost:8000/toggle-camera?status=${status}`, {
        method: 'POST'
      });
      const data = await res.json();
      setActive(data.camera_active);
      if (status) {
        setVideoUrl(`http://localhost:8000/video-feed?t=${new Date().getTime()}`);
      } else {
        setVideoUrl(null);
      }
    } catch (err) {
      alert("Error connecting to backend");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-12 bg-white min-h-screen p-4">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-800">Classroom Simulation</h2>
        <p className="text-gray-500 mt-2 max-w-lg mx-auto">
          Start the camera to begin real-time face detection, recognition, and automatic attendance marking.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full max-w-6xl">
        {/* Left Side: Camera Monitoring Controls */}
        <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 flex flex-col items-center justify-center">
          {!active ? (
            <button 
              onClick={() => toggleAttendance(true)}
              className="flex flex-col items-center group transition-all"
            >
              <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform shadow-lg shadow-blue-200">
                 <span className="text-4xl">📹</span>
              </div>
              <span className="text-xl font-bold text-blue-600">Start Camera Monitoring</span>
              <p className="text-sm text-gray-400 mt-1">(Real-time Recognition)</p>
            </button>
          ) : (
            <div className="flex flex-col items-center w-full">
               <div className="w-24 h-24 bg-green-500 rounded-full flex items-center justify-center text-white mb-4 animate-pulse shadow-lg shadow-green-200">
                  <span className="text-4xl text-white">●</span>
               </div>
               <span className="text-xl font-bold text-green-600 mb-6">Monitoring Active</span>
               <button 
                  onClick={() => toggleAttendance(false)}
                  className="bg-red-500 text-white px-8 py-3 rounded-full font-bold hover:bg-red-600 transition shadow-lg shadow-red-100"
               >
                  Stop Camera
               </button>
            </div>
          )}
        </div>

        {/* Right Side: Camera Real-Time Output */}
        <div className="bg-gray-900 rounded-2xl shadow-2xl overflow-hidden aspect-video flex items-center justify-center border-4 border-gray-800 relative">
          {active && videoUrl ? (
            <img 
              src={videoUrl} 
              alt="Live Feed" 
              className="w-full h-full object-cover"
              onError={() => toggleAttendance(false)}
            />
          ) : (
            <div className="text-center text-gray-500 p-8">
              <span className="text-6xl block mb-4">🌑</span>
              <p className="text-xl font-semibold">Camera Offline</p>
              <p className="text-sm">Click "Start Camera" to see the live recognition feed.</p>
            </div>
          )}
          {active && (
             <div className="absolute top-4 left-4 flex items-center space-x-2 bg-red-600 px-3 py-1 rounded-full">
                <div className="w-2 h-2 bg-white rounded-full animate-ping"></div>
                <span className="text-white text-xs font-bold">LIVE RECOGNITION</span>
             </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
         <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center text-center">
            <span className="font-bold text-blue-600 text-lg mb-1">Step 1</span>
            <p className="text-sm text-gray-600 font-medium">Position your face in the feed camera.</p>
         </div>
         <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center text-center">
            <span className="font-bold text-green-600 text-lg mb-1">Step 2</span>
            <p className="text-sm text-gray-600 font-medium">Automatic match with Student DB.</p>
         </div>
         <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center text-center">
            <span className="font-bold text-orange-600 text-lg mb-1">Step 3</span>
            <p className="text-sm text-gray-600 font-medium">Attendance marked for today.</p>
         </div>
      </div>
    </div>
  );
}
