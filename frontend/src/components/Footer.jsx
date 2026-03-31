import { Zap } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-navy-900 text-navy-300 border-t border-navy-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 bg-gradient-to-br from-accent-400 to-accent-600 rounded-lg flex items-center justify-center">
                <Zap className="w-4 h-4 text-white" />
              </div>
              <span className="text-white font-bold text-lg">AI Daily Pulse</span>
            </div>
            <p className="text-sm leading-relaxed">
              Your daily AI intelligence brief, curated from the best sources across the web.
              Stay informed, stay ahead.
            </p>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-3 text-sm uppercase tracking-wider">Sources</h3>
            <ul className="space-y-1.5 text-sm">
              <li>Reddit AI Communities</li>
              <li>Hacker News</li>
              <li>TechCrunch, The Verge, Wired</li>
              <li>ArXiv Research Papers</li>
              <li>Product Hunt</li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-3 text-sm uppercase tracking-wider">Delivery</h3>
            <ul className="space-y-1.5 text-sm">
              <li>Daily at 7:00 AM SAST</li>
              <li>Short email summary</li>
              <li>Detailed PDF report attached</li>
              <li>Full history on dashboard</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-navy-800 text-center text-xs text-navy-400">
          &copy; {new Date().getFullYear()} AI Daily Pulse. Powered by AI, curated for professionals.
        </div>
      </div>
    </footer>
  );
}
