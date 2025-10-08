# Ghost JSON Export Media Extractor

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Extract all images and videos from a Ghost blog JSON export file. Perfect for migrating from Ghost(Pro) to self-hosted.

**Zero web scraping. Zero API credits. 100% reliable.**

## Features

- ✅ Extracts media from Ghost JSON export (offline processing)
- ✅ Organizes downloads by post slug for easy migration
- ✅ Parallel downloads (10 workers)
- ✅ Automatic resume (skips existing files)
- ✅ Handles feature images + embedded media
- ✅ Supports images and videos
- ✅ Resolves `__GHOST_URL__` placeholders and relative URLs automatically

## Why This Over Web Scraping?

| Aspect | Web Scraping | JSON Export |
|--------|--------------|-------------|
| **API Credits** | 140+ (Firecrawl) | 0 (free!) |
| **Reliability** | ~95% | 100% |
| **Speed** | Network-bound | Instant parsing |
| **Risk** | May miss JS-rendered images | Zero risk |

## Installation

```bash
pip install -r requirements.txt
```

## Quick Test

Test the script with the included sample export:

```bash
python extract_media.py examples/ghost-export-sample.json --blog-url https://example-blog.com --dry-run
```

This sample demonstrates the `__GHOST_URL__` placeholder resolution.

## Usage

### 1. Export your Ghost blog

In Ghost Admin → Settings → Labs → Export your content

### 2. Extract media

**Important:** You must provide your blog URL with `--blog-url`. Ghost exports use `__GHOST_URL__` as a placeholder that needs to be replaced with your actual blog domain.

```bash
# Dry run (see what would be downloaded)
python extract_media.py ghost-export.json --blog-url https://yourblog.com --dry-run

# Download all media
python extract_media.py ghost-export.json --blog-url https://yourblog.com

# Custom output directory
python extract_media.py ghost-export.json --blog-url https://yourblog.com --output my-media
```

## Output Structure

```
images/
├── post-slug-1/
│   ├── feature-image.jpg
│   └── embedded-image.png
├── post-slug-2/
│   ├── header.jpg
│   ├── diagram.png
│   └── video.mp4
└── ...
```

Each post gets its own directory named by slug, containing all media from that post.

## What Gets Extracted

✅ **Feature images** (`feature_image` field)
✅ **Embedded images** (`<img>` tags in HTML)
✅ **Videos** (`<video>` and `<source>` tags)
❌ **Embeds** (YouTube iframes - not downloadable)
❌ **CSS backgrounds** (rare edge case)

## How It Works

1. Loads Ghost JSON export
2. Filters for published posts only (skips drafts)
3. For each post:
   - Extracts `feature_image` URL
   - Parses `html` field with BeautifulSoup
   - Finds all `<img>`, `<video>`, `<source>` tags
   - Replaces `__GHOST_URL__` placeholder with your blog URL
   - Resolves relative URLs to absolute
4. Downloads media in parallel (10 workers)
5. Organizes by post slug

## Requirements

- Python 3.8+
- `beautifulsoup4`
- `requests`

## Comparison with Firecrawl Approach

This repo focuses on **JSON export parsing** (simple, free, reliable).

For **web scraping** approach using Firecrawl, see: [ghost-produktiv-me-images](https://github.com/codeme-ne/ghost-produktiv-me-images)

## License

MIT

## Author

Built for migrating neurohackingly.com from Ghost(Pro) to self-hosted.
