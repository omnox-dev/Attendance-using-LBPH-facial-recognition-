"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [stats, setStats] = useState({ students: 0, attendance: 0 });

  useEffect(() => {
    fetch("http://localhost:8000/students")
      .then(res => res.json())
      .then(data => setStats(prev => ({ ...prev, students: data.length || 0 })))
      .catch(err => console.error("Error fetching students:", err));
    
    fetch("http://localhost:8000/attendance")
      .then(res => res.json())
      .then(data => setStats(prev => ({ ...prev, attendance: data.length || 0 })))
      .catch(err => console.error("Error fetching attendance:", err));
  }, []);

  const handleTrain = async () => {
    try {
      const res = await fetch('http://localhost:8000/train-model', { method: 'POST' });
      const data = await res.json();
      alert(data.message || 'Model Trained Successfully!');
    } catch (err) {
      alert("Error training model. Make sure backend is running.");
    }
  };

  return (
    <div className="space-y-6 bg-white min-h-screen p-4">
      <h2 className="text-3xl font-bold text-gray-800">Administrator Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center">
          <span className="text-4xl mb-2">👤</span>
          <h3 className="text-lg font-semibold text-gray-600">Total Students</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.students}</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center">
          <span className="text-4xl mb-2">✅</span>
          <h3 className="text-lg font-semibold text-gray-600">Total Attendance</h3>
          <p className="text-3xl font-bold text-green-600">{stats.attendance}</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex flex-col items-center cursor-pointer hover:bg-purple-50 transition-colors"
             onClick={handleTrain}>
          <span className="text-4xl mb-2">⚙️</span>
          <h3 className="text-lg font-semibold text-gray-600">Train Face Model</h3>
          <p className="text-sm text-gray-500 text-center">Re-train LBPH model with new images</p>
        </div>
      </div>
    </div>
  );
}

