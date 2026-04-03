import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import re

OUTPUT_DIR = Path("data/documents")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"}


def scrape_page(url: str, filename: str) -> bool:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"  X Failed {url}: {e}")
        return False

    soup = BeautifulSoup(response.text, "lxml")

    # Remove noise elements
    for tag in soup(
        ["nav", "header", "footer", "script", "style", "aside", "form", "button"]
    ):
        tag.decompose()

    # Try to get main article content first
    main = (
        soup.find("article")
        or soup.find("main")
        or soup.find(attrs={"role": "main"})
        or soup.find(class_=re.compile(r"content|article|post|doc", re.I))
        or soup.body
    )

    text = main.get_text(separator="\n", strip=True) if main else ""

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean = "\n".join(lines)

    if len(clean.split()) < 50:
        print(f"  X Too short ({len(clean.split())} words): {url}")
        return False

    out_path = OUTPUT_DIR / f"{filename}.txt"
    out_path.write_text(clean, encoding="utf-8")
    print(f"Saved {filename}.txt ({len(clean.split())} words)")
    return True


def scrape_all(pages: list[dict], delay: float = 1.5):
    success = 0
    for page in pages:
        result = scrape_page(page["url"], page["filename"])
        if result:
            success += 1
        time.sleep(delay)  # be polite — don't hammer servers
    print(f"\nDone: {success}/{len(pages)} pages saved.")


if __name__ == "__main__":
    # ← Edit this list with your chosen URLs
    PAGES = [
        {
            "url": "https://zapier.com/legal/terms-of-service",
            "filename": "zapier-terms",
        },
        {
            "url": "https://slack.com/help/articles/218080037-Getting-started-for-new-Slack-users",
            "filename": "slack-getting-started",
        },
        {
            "url": "https://intercom.com/help/en/articles/175-create-an-intercom-account",
            "filename": "intercom-create-account",
        },
        {
            "url": "https://slack.com/help/articles/218080037-Slack-plan-types-and-billing",
            "filename": "slack-billing",
        },
        {
            "url": "https://www.notion.so/help/billing-and-plans",
            "filename": "notion-billing",
        },
        {
            "url": "https://www.notion.so/help/delete-account-and-data",
            "filename": "notion-delete-account",
        },
        {
            "url": "https://www.notion.so/help/import-data-into-notion",
            "filename": "notion-import-data",
        },
        {
            "url": "https://www.notion.so/help/troubleshoot-notion",
            "filename": "notion-troubleshoot",
        },
        {"url": "https://linear.app/docs/faq", "filename": "linear-faq"},
        {"url": "https://linear.app/docs/security", "filename": "linear-security"},
        {"url": "https://www.figma.com/privacy/", "filename": "figma-privacy"},
        {
            "url": "https://help.figma.com/hc/en-us/articles/360040328273-Choose-a-Figma-plan",
            "filename": "figma-plans",
        },
        {
            "url": "https://help.figma.com/hc/en-us/articles/360039820114-Getting-started-in-Figma",
            "filename": "figma-getting-started",
        },
        {
            "url": "https://help.figma.com/hc/en-us/articles/360040314193-Contact-Figma-support",
            "filename": "figma-contact-support",
        },
    ]
    scrape_all(PAGES)
