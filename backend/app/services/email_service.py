import os
import base64
import logging
import resend
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _init_resend():
    resend.api_key = settings.resend_api_key


def send_daily_brief(
    to_emails: list[str],
    subject: str,
    short_summary_html: str,
    pdf_path: str | None = None,
) -> bool:
    if not settings.resend_api_key:
        logger.warning("Resend API key not configured — skipping email send")
        return False

    _init_resend()

    attachments = []
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = base64.b64encode(f.read()).decode("utf-8")
        attachments.append({
            "filename": os.path.basename(pdf_path),
            "content": pdf_data,
        })

    html_body = _build_email_html(short_summary_html)

    for email in to_emails:
        try:
            params = {
                "from": settings.from_email,
                "to": [email],
                "subject": subject,
                "html": html_body,
            }
            if attachments:
                params["attachments"] = attachments

            resend.Emails.send(params)
            logger.info(f"Email sent to {email}")
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            return False

    return True


def _build_email_html(summary_content: str) -> str:
    lines = summary_content.split("\n")
    html_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            html_lines.append(f"<li style='margin-bottom:6px;'>{stripped[2:]}</li>")
        elif stripped.startswith("**") and stripped.endswith("**"):
            html_lines.append(f"<p style='font-weight:bold;margin:12px 0 4px;'>{stripped.strip('*')}</p>")
        elif stripped == "":
            html_lines.append("<br>")
        else:
            import re
            formatted = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            html_lines.append(f"<p style='margin:4px 0;'>{formatted}</p>")

    body_content = "\n".join(html_lines)

    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0;padding:0;background-color:#f4f6f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f9;padding:20px 0;">
            <tr><td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
                    <!-- Header -->
                    <tr>
                        <td style="background:linear-gradient(135deg,#003366,#0066cc);padding:28px 32px;">
                            <h1 style="color:#ffffff;margin:0;font-size:24px;font-weight:700;">AI Daily Pulse</h1>
                            <p style="color:#b3d4fc;margin:4px 0 0;font-size:13px;">Your Daily AI Intelligence Brief</p>
                        </td>
                    </tr>
                    <!-- Body -->
                    <tr>
                        <td style="padding:28px 32px;color:#333333;font-size:14px;line-height:1.7;">
                            {body_content}
                        </td>
                    </tr>
                    <!-- PDF Notice -->
                    <tr>
                        <td style="padding:0 32px 20px;color:#666;font-size:13px;">
                            <div style="background:#f0f7ff;border-left:3px solid #0066cc;padding:12px 16px;border-radius:4px;">
                                📎 <strong>Detailed Report Attached</strong> — See the attached PDF for the full intelligence report with analysis, trends, and source articles.
                            </div>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background:#f8f9fa;padding:20px 32px;border-top:1px solid #eee;">
                            <p style="margin:0;font-size:12px;color:#999;text-align:center;">
                                AI Daily Pulse — Powered by AI, curated for professionals.<br>
                                <a href="#" style="color:#0066cc;text-decoration:none;">Unsubscribe</a> | <a href="#" style="color:#0066cc;text-decoration:none;">View in Browser</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td></tr>
        </table>
    </body>
    </html>
    """
