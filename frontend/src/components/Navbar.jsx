import { Link, useLocation } from "react-router-dom";
import { Zap, LayoutDashboard, Home } from "lucide-react";

export default function Navbar() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-navy-900 text-white sticky top-0 z-50 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 bg-gradient-to-br from-accent-400 to-accent-600 rounded-lg flex items-center justify-center shadow-md group-hover:shadow-accent-500/30 transition-shadow">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight">AI Daily Pulse</span>
              <span className="hidden sm:inline text-[11px] text-navy-300 ml-2 font-medium">Intelligence Brief</span>
            </div>
          </Link>

          <div className="flex items-center gap-1">
            <Link
              to="/"
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive("/")
                  ? "bg-navy-700 text-white"
                  : "text-navy-300 hover:bg-navy-800 hover:text-white"
              }`}
            >
              <Home className="w-4 h-4" />
              <span className="hidden sm:inline">Home</span>
            </Link>
            <Link
              to="/dashboard"
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive("/dashboard")
                  ? "bg-navy-700 text-white"
                  : "text-navy-300 hover:bg-navy-800 hover:text-white"
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span className="hidden sm:inline">Dashboard</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
