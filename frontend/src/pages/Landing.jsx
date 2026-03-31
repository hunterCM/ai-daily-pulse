import { useEffect, useState } from "react";
import {
  Zap, Newspaper, FileText, Clock, Shield, Globe,
  TrendingUp, Users, BookOpen, ArrowRight,
} from "lucide-react";
import { Link } from "react-router-dom";
import SubscribeForm from "../components/SubscribeForm";
import { api } from "../api/client";

const FEATURES = [
  {
    icon: Globe,
    title: "Multi-Platform Aggregation",
    desc: "Reddit, Hacker News, TechCrunch, The Verge, ArXiv, Product Hunt, and more — all in one place.",
  },
  {
    icon: Zap,
    title: "AI-Powered Summaries",
    desc: "GPT-4o distills hundreds of articles into clear, actionable intelligence you can read in minutes.",
  },
  {
    icon: FileText,
    title: "Detailed PDF Reports",
    desc: "Every email includes a comprehensive PDF with executive summaries, trends, and source links.",
  },
  {
    icon: Clock,
    title: "7 AM Daily Delivery",
    desc: "Arrives in your inbox before your workday starts, every morning at 7 AM SAST.",
  },
  {
    icon: BookOpen,
    title: "Searchable Archive",
    desc: "Full history of every brief on the dashboard. Never miss a story, even from weeks ago.",
  },
  {
    icon: Shield,
    title: "Professional Grade",
    desc: "Written for marketing leaders and executives. No fluff, just insights that matter.",
  },
];

const SOURCES = [
  "Reddit (r/artificial, r/MachineLearning, r/ChatGPT, +4 more)",
  "Hacker News — Top AI stories",
  "TechCrunch — AI Category",
  "The Verge — AI & Artificial Intelligence",
  "Ars Technica — Technology Lab",
  "MIT Technology Review",
  "VentureBeat — AI Category",
  "Wired — AI Coverage",
  "ArXiv — cs.AI, cs.LG, cs.CL Papers",
  "Product Hunt — AI Tools",
];

export default function Landing() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.getStats().then(setStats).catch(() => {});
  }, []);

  return (
    <div>
      {/* Hero */}
      <section className="relative bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900 text-white overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-accent-500 rounded-full blur-[120px]" />
          <div className="absolute bottom-10 right-20 w-96 h-96 bg-accent-400 rounded-full blur-[150px]" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 bg-navy-700/60 backdrop-blur rounded-full px-4 py-1.5 text-sm text-accent-400 font-medium mb-6">
              <Zap className="w-4 h-4" />
              AI news from 10+ sources, summarized daily
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight mb-5">
              Stay Ahead of the
              <span className="bg-gradient-to-r from-accent-400 to-cyan-300 text-transparent bg-clip-text"> AI Revolution</span>
            </h1>
            <p className="text-lg sm:text-xl text-navy-200 leading-relaxed mb-8 max-w-2xl">
              AI Daily Pulse curates the most important AI news from Reddit, Hacker News,
              TechCrunch, ArXiv, and more — then delivers a professional intelligence brief
              to your inbox every morning.
            </p>
            <div className="max-w-xl">
              <SubscribeForm />
            </div>
            <p className="text-navy-400 text-sm mt-3">
              Free forever. No spam. Unsubscribe anytime.
            </p>
          </div>
        </div>
      </section>

      {/* Stats */}
      {stats && (
        <section className="bg-white border-b border-gray-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="grid grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-2xl font-bold text-navy-900">{stats.total_subscribers || 0}</div>
                <div className="text-xs text-gray-500 font-medium uppercase tracking-wide mt-0.5">Subscribers</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-navy-900">{stats.total_briefs || 0}</div>
                <div className="text-xs text-gray-500 font-medium uppercase tracking-wide mt-0.5">Briefs Sent</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-navy-900">{stats.total_articles || 0}</div>
                <div className="text-xs text-gray-500 font-medium uppercase tracking-wide mt-0.5">Articles Analyzed</div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Features */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-bold text-navy-900 mb-3">
              Everything You Need to Stay Informed
            </h2>
            <p className="text-gray-500 text-lg max-w-2xl mx-auto">
              Built for busy professionals who need AI intelligence without the noise.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f) => (
              <div key={f.title} className="bg-white rounded-xl p-6 border border-gray-100 hover:shadow-lg hover:border-gray-200 transition-all">
                <div className="w-11 h-11 rounded-lg bg-accent-500/10 flex items-center justify-center mb-4">
                  <f.icon className="w-5.5 h-5.5 text-accent-600" />
                </div>
                <h3 className="font-semibold text-navy-900 text-lg mb-1.5">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Sources */}
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold text-navy-900 mb-4">
                10+ Sources, One Brief
              </h2>
              <p className="text-gray-500 text-lg mb-6">
                We scan the most important AI communities, publications, and research
                archives so you don't have to.
              </p>
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-2 text-accent-600 font-semibold hover:text-accent-700 transition-colors"
              >
                View the dashboard <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="space-y-2.5">
              {SOURCES.map((source, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 bg-gray-50 rounded-lg px-4 py-3 text-sm text-gray-700"
                >
                  <div className="w-2 h-2 rounded-full bg-accent-500 shrink-0" />
                  {source}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="bg-navy-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-bold mb-3">How It Works</h2>
            <p className="text-navy-300 text-lg">Three steps. Zero effort on your part.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: "01", title: "We Aggregate", desc: "Our system scans 10+ platforms every morning for the latest AI news, filtering out noise." },
              { step: "02", title: "AI Summarizes", desc: "GPT-4o analyzes and ranks the stories, generating an executive brief and detailed report." },
              { step: "03", title: "You Read", desc: "A short summary email + a detailed PDF lands in your inbox at 7 AM SAST. That's it." },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="text-5xl font-extrabold text-accent-500/30 mb-3">{item.step}</div>
                <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                <p className="text-navy-300 text-sm leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-r from-accent-500 to-accent-600 py-16">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-3">
            Start Your Morning Smarter
          </h2>
          <p className="text-white/80 text-lg mb-8">
            Join professionals who stay ahead of the AI curve with AI Daily Pulse.
          </p>
          <div className="max-w-lg mx-auto">
            <SubscribeForm />
          </div>
        </div>
      </section>
    </div>
  );
}
