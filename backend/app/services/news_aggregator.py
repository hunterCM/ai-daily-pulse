import httpx
import feedparser
import logging
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

AI_KEYWORDS = [
    "artificial intelligence", "machine learning", "deep learning", "neural network",
    "GPT", "LLM", "large language model", "ChatGPT", "OpenAI", "Anthropic", "Claude",
    "Gemini", "Midjourney", "Stable Diffusion", "generative AI", "AI agent",
    "transformer", "NLP", "computer vision", "reinforcement learning",
    "AI safety", "AI regulation", "AI startup", "foundation model",
]

REDDIT_SUBREDDITS = [
    "artificial", "MachineLearning", "ChatGPT", "OpenAI",
    "StableDiffusion", "LocalLLaMA", "singularity",
]

RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "Ars Technica AI": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "MIT Tech Review AI": "https://www.technologyreview.com/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "Wired AI": "https://www.wired.com/feed/tag/ai/latest/rss",
}


def _is_ai_related(title: str, summary: str = "") -> bool:
    text = f"{title} {summary}".lower()
    return any(kw.lower() in text for kw in AI_KEYWORDS)


async def fetch_reddit_posts() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        headers = {"User-Agent": settings.reddit_user_agent}

        token = None
        if settings.reddit_client_id and settings.reddit_client_secret:
            try:
                auth_resp = await client.post(
                    "https://www.reddit.com/api/v1/access_token",
                    data={"grant_type": "client_credentials"},
                    auth=(settings.reddit_client_id, settings.reddit_client_secret),
                    headers={"User-Agent": settings.reddit_user_agent},
                )
                if auth_resp.status_code == 200:
                    token = auth_resp.json().get("access_token")
            except Exception as e:
                logger.warning(f"Reddit OAuth failed, falling back to public API: {e}")

        for subreddit in REDDIT_SUBREDDITS:
            try:
                if token:
                    url = f"https://oauth.reddit.com/r/{subreddit}/hot?limit=15"
                    resp = await client.get(url, headers={
                        **headers, "Authorization": f"Bearer {token}"
                    })
                else:
                    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=15"
                    resp = await client.get(url, headers=headers)

                if resp.status_code != 200:
                    logger.warning(f"Reddit r/{subreddit} returned {resp.status_code}")
                    continue

                data = resp.json()
                for post in data.get("data", {}).get("children", []):
                    pd = post.get("data", {})
                    title = pd.get("title", "")
                    selftext = pd.get("selftext", "")[:500]

                    if not _is_ai_related(title, selftext) and subreddit not in [
                        "ChatGPT", "OpenAI", "StableDiffusion", "LocalLLaMA"
                    ]:
                        continue

                    created_utc = pd.get("created_utc", 0)
                    published = datetime.fromtimestamp(created_utc, tz=timezone.utc) if created_utc else None

                    if published and published < datetime.now(timezone.utc) - timedelta(days=2):
                        continue

                    articles.append({
                        "title": title,
                        "url": f"https://reddit.com{pd.get('permalink', '')}",
                        "source": f"Reddit r/{subreddit}",
                        "summary": selftext[:300] if selftext else "",
                        "score": pd.get("score", 0),
                        "author": pd.get("author", ""),
                        "published_at": published,
                        "category": "community",
                    })
            except Exception as e:
                logger.error(f"Error fetching r/{subreddit}: {e}")
    return articles


async def fetch_hackernews() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            story_ids = resp.json()[:50]

            for story_id in story_ids:
                try:
                    item_resp = await client.get(
                        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    )
                    item = item_resp.json()
                    if not item or item.get("type") != "story":
                        continue

                    title = item.get("title", "")
                    if not _is_ai_related(title):
                        continue

                    created = item.get("time", 0)
                    published = datetime.fromtimestamp(created, tz=timezone.utc) if created else None

                    if published and published < datetime.now(timezone.utc) - timedelta(days=2):
                        continue

                    articles.append({
                        "title": title,
                        "url": item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "source": "Hacker News",
                        "summary": "",
                        "score": item.get("score", 0),
                        "author": item.get("by", ""),
                        "published_at": published,
                        "category": "tech",
                    })
                except Exception as e:
                    logger.error(f"Error fetching HN item {story_id}: {e}")
        except Exception as e:
            logger.error(f"Error fetching Hacker News: {e}")
    return articles


async def fetch_rss_feeds() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        for source_name, feed_url in RSS_FEEDS.items():
            try:
                resp = await client.get(feed_url, headers={
                    "User-Agent": "AI Daily Pulse Bot/1.0"
                })
                if resp.status_code != 200:
                    logger.warning(f"RSS {source_name} returned {resp.status_code}")
                    continue

                feed = feedparser.parse(resp.text)
                for entry in feed.entries[:15]:
                    title = entry.get("title", "")
                    summary_raw = entry.get("summary", "")
                    summary_text = BeautifulSoup(summary_raw, "html.parser").get_text()[:300]

                    if not _is_ai_related(title, summary_text):
                        continue

                    published = None
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

                    if published and published < datetime.now(timezone.utc) - timedelta(days=2):
                        continue

                    articles.append({
                        "title": title,
                        "url": entry.get("link", ""),
                        "source": source_name,
                        "summary": summary_text,
                        "score": 0,
                        "author": entry.get("author", ""),
                        "published_at": published,
                        "category": "news",
                    })
            except Exception as e:
                logger.error(f"Error fetching RSS {source_name}: {e}")
    return articles


async def fetch_product_hunt() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(
                "https://www.producthunt.com/feed?category=artificial-intelligence",
                headers={"User-Agent": "AI Daily Pulse Bot/1.0"},
                follow_redirects=True,
            )
            if resp.status_code == 200:
                feed = feedparser.parse(resp.text)
                for entry in feed.entries[:10]:
                    title = entry.get("title", "")
                    summary_raw = entry.get("summary", "")
                    summary_text = BeautifulSoup(summary_raw, "html.parser").get_text()[:300]

                    articles.append({
                        "title": title,
                        "url": entry.get("link", ""),
                        "source": "Product Hunt",
                        "summary": summary_text,
                        "score": 0,
                        "author": entry.get("author", ""),
                        "published_at": None,
                        "category": "product",
                    })
        except Exception as e:
            logger.error(f"Error fetching Product Hunt: {e}")
    return articles


async def fetch_arxiv_papers() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL"
            url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=15"
            resp = await client.get(url)
            if resp.status_code == 200:
                feed = feedparser.parse(resp.text)
                for entry in feed.entries:
                    summary_text = entry.get("summary", "").replace("\n", " ")[:300]
                    articles.append({
                        "title": entry.get("title", "").replace("\n", " "),
                        "url": entry.get("link", ""),
                        "source": "ArXiv",
                        "summary": summary_text,
                        "score": 0,
                        "author": ", ".join(a.get("name", "") for a in entry.get("authors", [])[:3]),
                        "published_at": None,
                        "category": "research",
                    })
        except Exception as e:
            logger.error(f"Error fetching ArXiv: {e}")
    return articles


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    seen_titles = set()
    seen_urls = set()
    unique = []
    for article in articles:
        title_key = article["title"].lower().strip()[:80]
        url_key = article["url"].split("?")[0]
        if title_key not in seen_titles and url_key not in seen_urls:
            seen_titles.add(title_key)
            seen_urls.add(url_key)
            unique.append(article)
    return unique


def rank_articles(articles: list[dict], max_articles: int = 30) -> list[dict]:
    source_weights = {
        "Hacker News": 1.5,
        "TechCrunch AI": 1.4,
        "The Verge AI": 1.3,
        "ArXiv": 1.2,
        "Product Hunt": 1.1,
    }

    for article in articles:
        base_score = article.get("score", 0)
        weight = 1.0
        for source_key, w in source_weights.items():
            if source_key in article.get("source", ""):
                weight = w
                break
        if article.get("source", "").startswith("Reddit"):
            weight = 1.0 + min(base_score / 1000, 1.0)
        article["_rank_score"] = base_score * weight

    articles.sort(key=lambda a: a["_rank_score"], reverse=True)
    for article in articles:
        article.pop("_rank_score", None)

    return articles[:max_articles]


async def aggregate_all_news() -> list[dict]:
    import asyncio

    results = await asyncio.gather(
        fetch_reddit_posts(),
        fetch_hackernews(),
        fetch_rss_feeds(),
        fetch_product_hunt(),
        fetch_arxiv_papers(),
        return_exceptions=True,
    )

    all_articles = []
    source_names = ["Reddit", "Hacker News", "RSS Feeds", "Product Hunt", "ArXiv"]
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Error from {source_names[i]}: {result}")
        else:
            all_articles.extend(result)
            logger.info(f"Fetched {len(result)} articles from {source_names[i]}")

    unique = deduplicate_articles(all_articles)
    ranked = rank_articles(unique)
    logger.info(f"Total: {len(all_articles)} raw -> {len(unique)} unique -> {len(ranked)} top articles")
    return ranked
