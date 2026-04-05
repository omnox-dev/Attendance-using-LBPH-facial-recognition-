"use client";

import { useEffect, useState } from "react";

export default function ReportsPage() {
  const [attendance, setAttendance] = useState<any[]>([]);

  const fetchAttendance = () => {
    fetch("http://localhost:8000/attendance")
      .then(res => res.json())
      .then(data => setAttendance(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchAttendance();
  }, []);

  const handleDownload = () => {
    window.open("http://localhost:8000/export-csv");
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Attendance Reports</h2>
        <button 
          onClick={handleDownload}
          className="bg-green-600 text-white px-6 py-2 rounded-lg shadow-md hover:bg-green-700 transition flex items-center space-x-2"
        >
          <span>📥</span>
          <span>Download CSV Report</span>
        </button>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="p-4 font-semibold text-gray-700">DATE</th>
                <th className="p-4 font-semibold text-gray-700">TIME</th>
                <th className="p-4 font-semibold text-gray-700">NAME</th>
                <th className="p-4 font-semibold text-gray-700">ROLL NO</th>
                <th className="p-4 font-semibold text-gray-700">STATUS</th>
              </tr>
            </thead>
            <tbody>
              {attendance.map((record, index) => (
                <tr key={index} className="border-b hover:bg-gray-50 transition-colors">
                  <td className="p-4 text-gray-600 font-medium">{record.date}</td>
                  <td className="p-4 text-gray-500">{record.time}</td>
                  <td className="p-4 text-gray-900 font-bold">{record.name}</td>
                  <td className="p-4 text-gray-600">{record.roll_number}</td>
                  <td className="p-4">
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">
                        {record.status}
                    </span>
                  </td>
                </tr>
              ))}
              {attendance.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center p-12 text-gray-400">No attendance entries recorded today. Start the camera and show your face!</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
