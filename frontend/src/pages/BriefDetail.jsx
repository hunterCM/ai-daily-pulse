import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft, Download, Calendar, Newspaper, Send,
  Loader2, ExternalLink,
} from "lucide-react";
import { format } from "date-fns";
import ReactMarkdown from "react-markdown";
import NewsCard from "../components/NewsCard";
import { api } from "../api/client";

export default function BriefDetail() {
  const { id } = useParams();
  const [brief, setBrief] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState("summary");

  useEffect(() => {
    setLoading(true);
    api
      .getBrief(id)
      .then(setBrief)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-accent-500" />
      </div>
    );
  }

  if (!brief) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold text-gray-700 mb-2">Brief Not Found</h2>
        <p className="text-gray-400 mb-6">This brief may not exist or has been removed.</p>
        <Link
          to="/dashboard"
          className="text-accent-600 hover:text-accent-700 font-medium inline-flex items-center gap-1"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back + Header */}
      <Link
        to="/dashboard"
        className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 font-medium mb-6"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Dashboard
      </Link>

      <div className="bg-gradient-to-br from-navy-900 to-navy-800 rounded-2xl p-6 sm:p-8 text-white mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold mb-2">
              AI Daily Pulse
            </h1>
            <div className="flex items-center gap-4 text-navy-300 text-sm">
              <span className="flex items-center gap-1.5">
                <Calendar className="w-4 h-4" />
                {format(new Date(brief.date), "EEEE, MMMM d, yyyy")}
              </span>
              <span className="flex items-center gap-1.5">
                <Newspaper className="w-4 h-4" />
                {brief.articles.length} articles
              </span>
              <span className="flex items-center gap-1.5">
                <Send className="w-4 h-4" />
                {brief.sent ? `Sent to ${brief.subscriber_count}` : "Draft"}
              </span>
            </div>
          </div>
          <a
            href={`/api/briefs/${brief.id}/pdf`}
            className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 backdrop-blur rounded-lg px-5 py-2.5 text-sm font-medium transition-colors"
          >
            <Download className="w-4 h-4" />
            Download PDF
          </a>
        </div>
      </div>

      {/* View Toggle */}
      <div className="flex gap-1 bg-gray-100 rounded-lg p-1 mb-6 w-fit">
        {[
          { id: "summary", label: "Quick Summary" },
          { id: "full", label: "Full Report" },
          { id: "articles", label: "Source Articles" },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveView(tab.id)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer ${
              activeView === tab.id
                ? "bg-white text-navy-900 shadow-sm"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Quick Summary */}
      {activeView === "summary" && (
        <div className="bg-white rounded-xl border border-gray-100 p-6 sm:p-8">
          <div className="prose prose-sm max-w-none prose-headings:text-navy-900 prose-a:text-accent-600">
            <ReactMarkdown>{brief.short_summary || "No summary available."}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Full Report */}
      {activeView === "full" && (
        <div className="bg-white rounded-xl border border-gray-100 p-6 sm:p-8">
          <div className="prose max-w-none prose-headings:text-navy-900 prose-a:text-accent-600 prose-strong:text-navy-800">
            <ReactMarkdown>{brief.full_summary || "No full report available."}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Source Articles */}
      {activeView === "articles" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {brief.articles.length === 0 ? (
            <div className="col-span-full bg-white rounded-xl border border-gray-100 p-12 text-center text-gray-400">
              No source articles linked to this brief.
            </div>
          ) : (
            brief.articles.map((article) => (
              <NewsCard key={article.id} article={article} />
            ))
          )}
        </div>
      )}
    </div>
  );
}
