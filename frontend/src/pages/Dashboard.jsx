import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Calendar, FileText, Users, Newspaper, Loader2,
  ChevronRight, RefreshCw, Filter,
} from "lucide-react";
import { format } from "date-fns";
import NewsCard from "../components/NewsCard";
import { api } from "../api/client";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [briefs, setBriefs] = useState([]);
  const [articles, setArticles] = useState([]);
  const [sources, setSources] = useState([]);
  const [selectedSource, setSelectedSource] = useState("");
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [activeTab, setActiveTab] = useState("briefs");

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (activeTab === "articles") {
      loadArticles();
    }
  }, [selectedSource, activeTab]);

  async function loadData() {
    setLoading(true);
    try {
      const [statsData, briefsData, sourcesData] = await Promise.all([
        api.getStats().catch(() => null),
        api.getBriefs().catch(() => []),
        api.getSources().catch(() => []),
      ]);
      setStats(statsData);
      setBriefs(briefsData);
      setSources(sourcesData);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    }
    setLoading(false);
  }

  async function loadArticles() {
    try {
      const data = await api.getArticles(0, 50, selectedSource || undefined);
      setArticles(data);
    } catch (err) {
      console.error("Failed to load articles:", err);
    }
  }

  async function handleTriggerBrief() {
    if (triggering) return;
    setTriggering(true);
    try {
      await api.triggerBrief();
      setTimeout(loadData, 3000);
    } catch (err) {
      console.error("Failed to trigger brief:", err);
    }
    setTriggering(false);
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-accent-500" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-navy-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">Your AI news intelligence center</p>
        </div>
        <button
          onClick={handleTriggerBrief}
          disabled={triggering}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-navy-900 hover:bg-navy-800 text-white rounded-lg font-medium text-sm transition-colors disabled:opacity-60 cursor-pointer disabled:cursor-not-allowed"
        >
          <RefreshCw className={`w-4 h-4 ${triggering ? "animate-spin" : ""}`} />
          {triggering ? "Generating..." : "Generate Brief Now"}
        </button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { icon: Users, label: "Subscribers", value: stats.total_subscribers, color: "text-blue-600 bg-blue-50" },
            { icon: FileText, label: "Briefs", value: stats.total_briefs, color: "text-emerald-600 bg-emerald-50" },
            { icon: Newspaper, label: "Articles", value: stats.total_articles, color: "text-amber-600 bg-amber-50" },
            {
              icon: Calendar,
              label: "Latest Brief",
              value: stats.latest_brief_date ? format(new Date(stats.latest_brief_date), "MMM d") : "None",
              color: "text-purple-600 bg-purple-50",
            },
          ].map((stat) => (
            <div key={stat.label} className="bg-white rounded-xl border border-gray-100 p-5">
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stat.color}`}>
                  <stat.icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-2xl font-bold text-navy-900">{stat.value}</div>
                  <div className="text-xs text-gray-500 font-medium">{stat.label}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 rounded-lg p-1 mb-6 w-fit">
        {[
          { id: "briefs", label: "Briefs History", icon: FileText },
          { id: "articles", label: "All Articles", icon: Newspaper },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer ${
              activeTab === tab.id
                ? "bg-white text-navy-900 shadow-sm"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Briefs History */}
      {activeTab === "briefs" && (
        <div className="space-y-3">
          {briefs.length === 0 ? (
            <div className="bg-white rounded-xl border border-gray-100 p-12 text-center">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <h3 className="text-lg font-semibold text-gray-700 mb-1">No briefs yet</h3>
              <p className="text-gray-400 text-sm mb-4">
                Click "Generate Brief Now" to create your first AI Daily Pulse brief.
              </p>
            </div>
          ) : (
            briefs.map((brief) => (
              <Link
                key={brief.id}
                to={`/brief/${brief.id}`}
                className="flex items-center justify-between bg-white rounded-xl border border-gray-100 p-5 hover:shadow-md hover:border-gray-200 transition-all group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-lg bg-navy-50 flex flex-col items-center justify-center">
                    <span className="text-xs font-bold text-navy-600">
                      {format(new Date(brief.date), "MMM")}
                    </span>
                    <span className="text-lg font-bold text-navy-900 leading-none">
                      {format(new Date(brief.date), "d")}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-navy-900 group-hover:text-accent-600 transition-colors">
                      AI Daily Pulse — {format(new Date(brief.date), "EEEE, MMMM d, yyyy")}
                    </h3>
                    <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
                      <span>{brief.article_count} articles</span>
                      <span className={brief.sent ? "text-emerald-500" : "text-amber-500"}>
                        {brief.sent ? "Sent" : "Draft"}
                      </span>
                    </div>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-300 group-hover:text-accent-500 transition-colors" />
              </Link>
            ))
          )}
        </div>
      )}

      {/* Articles */}
      {activeTab === "articles" && (
        <div>
          {sources.length > 0 && (
            <div className="flex items-center gap-2 mb-5 flex-wrap">
              <Filter className="w-4 h-4 text-gray-400" />
              <button
                onClick={() => setSelectedSource("")}
                className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors cursor-pointer ${
                  !selectedSource
                    ? "bg-navy-900 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                All
              </button>
              {sources.map((source) => (
                <button
                  key={source}
                  onClick={() => setSelectedSource(source)}
                  className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors cursor-pointer ${
                    selectedSource === source
                      ? "bg-navy-900 text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {source}
                </button>
              ))}
            </div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {articles.length === 0 ? (
              <div className="col-span-full bg-white rounded-xl border border-gray-100 p-12 text-center">
                <Newspaper className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-700 mb-1">No articles yet</h3>
                <p className="text-gray-400 text-sm">
                  Articles will appear here after the first brief is generated.
                </p>
              </div>
            ) : (
              articles.map((article) => (
                <NewsCard key={article.id} article={article} />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
