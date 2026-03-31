import { ExternalLink, TrendingUp, Clock } from "lucide-react";
import { format } from "date-fns";

const SOURCE_COLORS = {
  Reddit: "bg-orange-100 text-orange-700",
  "Hacker News": "bg-amber-100 text-amber-700",
  TechCrunch: "bg-emerald-100 text-emerald-700",
  "The Verge": "bg-purple-100 text-purple-700",
  ArXiv: "bg-red-100 text-red-700",
  "Product Hunt": "bg-rose-100 text-rose-700",
  Wired: "bg-gray-100 text-gray-700",
  MIT: "bg-sky-100 text-sky-700",
  VentureBeat: "bg-indigo-100 text-indigo-700",
  Ars: "bg-teal-100 text-teal-700",
};

function getSourceColor(source) {
  for (const [key, value] of Object.entries(SOURCE_COLORS)) {
    if (source.includes(key)) return value;
  }
  return "bg-gray-100 text-gray-700";
}

export default function NewsCard({ article }) {
  return (
    <article className="bg-white rounded-xl border border-gray-100 p-5 hover:shadow-md hover:border-gray-200 transition-all group">
      <div className="flex items-start justify-between gap-3 mb-2.5">
        <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-semibold ${getSourceColor(article.source)}`}>
          {article.source}
        </span>
        {article.score > 0 && (
          <span className="flex items-center gap-1 text-xs text-gray-400 shrink-0">
            <TrendingUp className="w-3.5 h-3.5" />
            {article.score.toLocaleString()}
          </span>
        )}
      </div>

      <h3 className="font-semibold text-gray-900 text-[15px] leading-snug mb-2 group-hover:text-accent-600 transition-colors">
        <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
          {article.title}
        </a>
      </h3>

      {article.summary && (
        <p className="text-sm text-gray-500 leading-relaxed line-clamp-2 mb-3">
          {article.summary}
        </p>
      )}

      <div className="flex items-center justify-between text-xs text-gray-400">
        <div className="flex items-center gap-3">
          {article.author && <span>by {article.author}</span>}
          {article.published_at && (
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {format(new Date(article.published_at), "MMM d, h:mm a")}
            </span>
          )}
        </div>
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1 text-accent-500 hover:text-accent-600 font-medium"
        >
          Read <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </article>
  );
}
