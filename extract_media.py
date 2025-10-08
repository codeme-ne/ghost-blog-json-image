#!/usr/bin/env python3
"""
Ghost JSON Export Media Extractor

Extracts all images and videos from a Ghost blog JSON export file.
Organizes downloaded media by post slug for easy migration.

Zero web scraping. Zero API credits. 100% reliable.
"""

import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import sys

# Configuration
BLOG_URL = "https://neurohackingly.com"
MAX_WORKERS = 10
DOWNLOAD_TIMEOUT = 30
CHUNK_SIZE = 8192


def resolve_ghost_url(url, blog_url):
    """
    Replace Ghost's __GHOST_URL__ placeholder with actual blog URL.

    Ghost JSON exports use __GHOST_URL__ as a placeholder that needs
    to be replaced with the actual blog domain.

    Args:
        url: URL that may contain __GHOST_URL__ placeholder
        blog_url: Actual blog URL to use as replacement

    Returns:
        str: URL with __GHOST_URL__ replaced
    """
    if url and '__GHOST_URL__' in url:
        return url.replace('__GHOST_URL__', blog_url)
    return url


def parse_ghost_export(file_path):
    """
    Parse Ghost JSON export and extract media URLs for each published post.

    Returns:
        dict: {slug: [media_urls]}
    """
    print(f"📖 Loading Ghost export: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Navigate the nested structure
    posts = data.get('db', [{}])[0].get('data', {}).get('posts', [])
    print(f"📊 Found {len(posts)} total posts in export")

    urls_by_slug = {}
    published_count = 0

    for post in posts:
        # Only process published posts
        if post.get('status') != 'published':
            continue

        published_count += 1
        slug = post.get('slug')
        if not slug:
            continue

        media_urls = set()

        # 1. Extract feature image
        if feature_image := post.get('feature_image'):
            resolved_url = resolve_ghost_url(feature_image, BLOG_URL)
            media_urls.add(urljoin(BLOG_URL, resolved_url))

        # 2. Parse HTML content for embedded media
        html_content = post.get('html')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract images
            for img in soup.find_all('img'):
                if src := img.get('src'):
                    # Resolve __GHOST_URL__ placeholder and convert to absolute
                    resolved_url = resolve_ghost_url(src, BLOG_URL)
                    media_urls.add(urljoin(BLOG_URL, resolved_url))

            # Extract videos and their sources
            for video in soup.find_all('video'):
                if src := video.get('src'):
                    resolved_url = resolve_ghost_url(src, BLOG_URL)
                    media_urls.add(urljoin(BLOG_URL, resolved_url))
                for source in video.find_all('source'):
                    if src := source.get('src'):
                        resolved_url = resolve_ghost_url(src, BLOG_URL)
                        media_urls.add(urljoin(BLOG_URL, resolved_url))

        urls_by_slug[slug] = list(media_urls)

    print(f"✅ Found {published_count} published posts")
    print(f"📁 Will create {len(urls_by_slug)} directories")

    return urls_by_slug


def download_file(url, filepath):
    """Download a single file with streaming."""
    try:
        response = requests.get(url, stream=True, timeout=DOWNLOAD_TIMEOUT)
        response.raise_for_status()

        # Create parent directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        return True, url, None
    except Exception as e:
        return False, url, str(e)


def download_media(urls_by_slug, output_dir="images", dry_run=False):
    """
    Download all media files organized by post slug.

    Args:
        urls_by_slug: Dict of {slug: [media_urls]}
        output_dir: Base directory for downloads
        dry_run: If True, only print what would be downloaded
    """
    Path(output_dir).mkdir(exist_ok=True)

    # Prepare download tasks
    tasks = []
    for slug, urls in urls_by_slug.items():
        slug_dir = os.path.join(output_dir, slug)

        for url in urls:
            # Extract filename from URL
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "unnamed_file"

            filepath = os.path.join(slug_dir, filename)

            # Skip if already exists
            if os.path.exists(filepath):
                continue

            tasks.append((url, filepath))

    total_files = len(tasks)
    print(f"\n📥 {total_files} files to download")

    if dry_run:
        print("🔍 DRY RUN - Would download:")
        for url, filepath in tasks[:10]:  # Show first 10
            print(f"  {filepath}")
        if total_files > 10:
            print(f"  ... and {total_files - 10} more")
        return

    # Download in parallel
    success_count = 0
    error_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_file, url, filepath): (url, filepath)
                   for url, filepath in tasks}

        for i, future in enumerate(as_completed(futures), 1):
            success, url, error = future.result()

            if success:
                success_count += 1
            else:
                error_count += 1
                print(f"❌ Failed: {url[:50]}... - {error}")

            # Progress update every 10 files
            if i % 10 == 0 or i == total_files:
                print(f"Progress: {i}/{total_files} ({success_count} ✅, {error_count} ❌)")

    print(f"\n🎉 Download complete!")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Failed: {error_count}")
    print(f"   📁 Output: {output_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description="Extract media from Ghost JSON export"
    )
    parser.add_argument(
        'json_file',
        help='Path to Ghost JSON export file'
    )
    parser.add_argument(
        '--output',
        default='images',
        help='Output directory (default: images)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be downloaded without downloading'
    )
    parser.add_argument(
        '--blog-url',
        required=True,
        help='Your blog URL (e.g., https://yourblog.com) - required for resolving __GHOST_URL__ placeholders and relative paths'
    )

    args = parser.parse_args()

    # Update global BLOG_URL with provided value
    global BLOG_URL
    BLOG_URL = args.blog_url

    # Validate input file
    if not os.path.exists(args.json_file):
        print(f"❌ Error: File not found: {args.json_file}")
        sys.exit(1)

    try:
        # Parse JSON export
        urls_by_slug = parse_ghost_export(args.json_file)

        if not urls_by_slug:
            print("⚠️  No published posts found with media")
            return

        # Download media
        download_media(urls_by_slug, args.output, args.dry_run)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
