#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path
import urllib.request

def to_snake_case(title: str) -> str:
    """Convert title to snake_case, strip leading articles."""
    title = re.sub(r'^(The|A|An)\s+', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[^a-zA-Z0-9]+', '_', title.strip())
    title = re.sub(r'_+', '_', title)
    return title.lower().strip('_')


def clean_gutenberg_text(text: str) -> str:
    """Strip standard Project Gutenberg header and footer."""
    start_match = re.search(r'\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*', 
                           text, re.IGNORECASE | re.DOTALL)
    end_match = re.search(r'\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*', 
                         text, re.IGNORECASE | re.DOTALL)
    
    if start_match and end_match:
        cleaned = text[start_match.end():end_match.start()].strip()
    elif start_match:
        cleaned = text[start_match.end():].strip()
    else:
        cleaned = text.strip()
    
    cleaned = re.sub(r'^\s*\n+', '', cleaned)
    cleaned = re.sub(r'\n+\s*$', '', cleaned)
    return cleaned


def download_book(url: str) -> None:
    print(f"📥 Downloading: {url}")
    try:
        with urllib.request.urlopen(url, timeout=45) as resp:
            text = resp.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return

    # Extract Title
    title_match = re.search(r'^Title:\s*(.+?)$', text, re.MULTILINE | re.IGNORECASE)
    if title_match:
        raw_title = title_match.group(1).strip()
        filename = to_snake_case(raw_title) + ".txt"
        print(f"   Title: {raw_title} → {filename}")
    else:
        filename = Path(url).name
        if not filename.endswith('.txt'):
            filename += ".txt"
        print(f"   No Title found → using {filename}")

    clean_text = clean_gutenberg_text(text)
    Path(filename).write_text(clean_text, encoding='utf-8')
    
    print(f"✅ Saved {len(clean_text):,} chars → {filename}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Download & clean Project Gutenberg books",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python download_gutenberg.py <url>
  python download_gutenberg.py url1 url2 ...
  python download_gutenberg.py -i books.txt
  cat books.txt | python download_gutenberg.py"""
    )
    
    parser.add_argument('urls', nargs='*', help='One or more Gutenberg raw text URLs')
    parser.add_argument('-i', '--input-file', type=argparse.FileType('r'),
                        help='File containing one URL per line')
    
    args = parser.parse_args()

    # Collect all URLs
    url_list = []

    # 1. From --input-file
    if args.input_file:
        url_list.extend(line.strip() for line in args.input_file if line.strip() and not line.startswith('#'))

    # 2. From stdin (pipe or redirect)
    if not sys.stdin.isatty():
        for line in sys.stdin:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                url_list.append(stripped)

    # 3. From command-line arguments
    url_list.extend(args.urls)

    if not url_list:
        parser.print_help()
        print("\n❌ No URLs provided.")
        sys.exit(1)

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = [u for u in url_list if not (u in seen or seen.add(u))]

    print(f"Found {len(unique_urls)} unique book URL(s) to download.\n")
    
    for url in unique_urls:
        if url:
            download_book(url.strip())


if __name__ == "__main__":
    main()
