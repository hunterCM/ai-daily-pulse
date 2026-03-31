import logging
from openai import AsyncOpenAI
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=settings.openai_api_key)


async def summarize_articles(articles: list[dict]) -> dict:
    """Generate both a short email summary and a detailed full summary."""
    if not settings.openai_api_key:
        return _fallback_summary(articles)

    client = _get_client()
    articles_text = _format_articles_for_prompt(articles)

    short_summary = await _generate_short_summary(client, articles_text)
    full_summary = await _generate_full_summary(client, articles_text)

    return {
        "short_summary": short_summary,
        "full_summary": full_summary,
    }


def _format_articles_for_prompt(articles: list[dict]) -> str:
    lines = []
    for i, article in enumerate(articles, 1):
        source = article.get("source", "Unknown")
        title = article.get("title", "")
        summary = article.get("summary", "")
        score = article.get("score", 0)
        url = article.get("url", "")
        lines.append(f"{i}. [{source}] {title}\n   Score: {score} | URL: {url}\n   {summary}\n")
    return "\n".join(lines)


async def _generate_short_summary(client: AsyncOpenAI, articles_text: str) -> str:
    try:
        resp = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional AI industry analyst writing a daily brief "
                        "for a lead marketer. Your tone is professional, concise, and insightful. "
                        "Focus on what matters for business and marketing professionals."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Based on the following AI news articles from today, write a SHORT "
                        f"email-friendly summary. Include:\n"
                        f"- A one-line greeting ('Good morning, here's your AI Daily Pulse for [date]')\n"
                        f"- Top 5-8 stories as bullet points (one line each, with source)\n"
                        f"- A one-sentence 'Bottom Line' takeaway\n"
                        f"- Keep it under 300 words total\n\n"
                        f"Today's articles:\n{articles_text}"
                    ),
                },
            ],
            max_tokens=800,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"OpenAI short summary failed: {e}")
        return _fallback_short(articles_text)


async def _generate_full_summary(client: AsyncOpenAI, articles_text: str) -> str:
    try:
        resp = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior AI industry analyst preparing a comprehensive daily "
                        "intelligence report. Write in a professional, authoritative tone suitable "
                        "for C-suite executives and marketing leaders. Use clear section headers "
                        "and structured formatting."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Write a DETAILED AI Daily Intelligence Report based on these articles. "
                        f"Structure it as follows:\n\n"
                        f"# AI Daily Pulse — Intelligence Report\n\n"
                        f"## Executive Summary\n"
                        f"(3-4 sentences overview of the day's most important developments)\n\n"
                        f"## Top Stories\n"
                        f"(For each major story: headline, 2-3 sentence analysis, source, and link)\n\n"
                        f"## Industry Trends\n"
                        f"(Identify 2-3 emerging patterns across today's news)\n\n"
                        f"## Marketing & Business Impact\n"
                        f"(What marketers and business leaders should pay attention to)\n\n"
                        f"## Research & Development\n"
                        f"(Notable papers or technical breakthroughs, explained simply)\n\n"
                        f"## New Tools & Products\n"
                        f"(New AI tools launched or updated)\n\n"
                        f"## Key Takeaways\n"
                        f"(3-5 bullet points of actionable insights)\n\n"
                        f"Articles:\n{articles_text}"
                    ),
                },
            ],
            max_tokens=3000,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"OpenAI full summary failed: {e}")
        return _fallback_full(articles_text)


def _fallback_summary(articles: list[dict]) -> dict:
    return {
        "short_summary": _fallback_short(_format_articles_for_prompt(articles)),
        "full_summary": _fallback_full(_format_articles_for_prompt(articles)),
    }


def _fallback_short(articles_text: str) -> str:
    return (
        "Good morning! Here's your AI Daily Pulse.\n\n"
        "Today's top AI stories:\n\n"
        f"{articles_text[:1000]}\n\n"
        "Note: AI summarization unavailable — showing raw headlines. "
        "Configure your OpenAI API key for intelligent summaries."
    )


def _fallback_full(articles_text: str) -> str:
    return (
        "# AI Daily Pulse — Intelligence Report\n\n"
        "## Today's Articles\n\n"
        f"{articles_text}\n\n"
        "---\n"
        "Note: AI summarization unavailable. Configure your OpenAI API key "
        "for detailed analysis and insights."
    )
