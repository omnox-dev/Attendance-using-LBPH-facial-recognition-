import "./globals.css";
import Link from "next/link";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900 transition-colors duration-200">
        <nav className="bg-blue-600 text-white p-4 shadow-md flex justify-between items-center">
          <h1 className="text-xl font-bold">Face Recognition Attendance</h1>
          <div className="flex space-x-6">
            <Link href="/" className="hover:text-blue-200">Dashboard</Link>
            <Link href="/students" className="hover:text-blue-200">Students</Link>
            <Link href="/attendance" className="hover:text-blue-200">Start Attendance</Link>
            <Link href="/reports" className="hover:text-blue-200">Reports</Link>
          </div>
        </nav>
        <main className="container mx-auto p-4 lg:p-8">
          {children}
        </main>
        <footer className="bg-gray-800 text-gray-400 text-center p-4 mt-8">
          &copy; 2026 Academic Minor Project - Face Recognition System
        </footer>
      </body>
    </html>
  );
}
