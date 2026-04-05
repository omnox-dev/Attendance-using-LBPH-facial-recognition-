"use client";

import { useEffect, useState } from "react";

export default function StudentsPage() {
  const [students, setStudents] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [roll, setRoll] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchStudents = () => {
    fetch("http://localhost:8000/students")
      .then(res => res.json())
      .then(data => setStudents(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/register-student?name=${encodeURIComponent(name)}&roll_number=${encodeURIComponent(roll)}`, {
        method: 'POST'
      });
      const data = await res.json();
      if (res.ok) {
        alert("Student registered. Webcam will now open to capture 30 images.");
        setName("");
        setRoll("");
        fetchStudents();
      } else {
        alert(data.detail || "Registration failed");
      }
    } catch (err) {
      alert("Error connecting to backend");
    }
    setLoading(false);
  };

  const deleteStudent = async (id: number) => {
    if (!confirm("Are you sure? This will delete the student, their images, and ALL their attendance records.")) return;
    try {
      const res = await fetch(`http://localhost:8000/delete-student/${id}`, { method: 'DELETE' });
      if (res.ok) {
        fetchStudents();
        alert("Student deleted successfully.");
      } else {
        alert("Delete failed.");
      }
    } catch (err) {
      alert("Cannot connect to server.");
    }
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <h2 className="text-2xl font-bold mb-4">Register New Student</h2>
        <form onSubmit={handleRegister} className="flex flex-col md:flex-row gap-4">
          <input 
            type="text" 
            placeholder="Student Name" 
            className="border p-2 rounded flex-grow"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input 
            type="text" 
            placeholder="Roll Number" 
            className="border p-2 rounded flex-grow"
            value={roll}
            onChange={(e) => setRoll(e.target.value)}
            required
          />
          <button 
            type="submit" 
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
            disabled={loading}
          >
            {loading ? "Processing..." : "Register & Capture"}
          </button>
        </form>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <h2 className="text-2xl font-bold mb-4">Registered Students</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b">
                <th className="p-2">ID</th>
                <th className="p-2">Name</th>
                <th className="p-2">Roll Number</th>
                <th className="p-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {students.map(s => (
                <tr key={s.id} className="border-b hover:bg-gray-50">
                  <td className="p-2">{s.id}</td>
                  <td className="p-2">{s.name}</td>
                  <td className="p-2">{s.roll_number}</td>
                  <td className="p-2">
                    <button 
                      onClick={() => deleteStudent(s.id)}
                      className="text-red-500 hover:text-red-700 font-bold px-2 py-1 rounded border border-red-200"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              {students.length === 0 && (
                <tr>
                  <td colSpan={4} className="text-center p-4 text-gray-500">No students registered yet.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
