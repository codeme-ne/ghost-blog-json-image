# Ghost JSON Export Media Extractor

Extract all images and videos from a Ghost blog JSON export file. Perfect for migrating from Ghost(Pro) to self-hosted.

**Zero web scraping. Zero API credits. 100% reliable.**

## Features

- ✅ Extracts media from Ghost JSON export (offline processing)
- ✅ Organizes downloads by post slug for easy migration
- ✅ Parallel downloads (10 workers)
- ✅ Automatic resume (skips existing files)
- ✅ Handles feature images + embedded media
- ✅ Supports images and videos
- ✅ Resolves relative URLs automatically

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

## Usage

### 1. Export your Ghost blog

In Ghost Admin → Settings → Labs → Export your content

### 2. Extract media

```bash
# Dry run (see what would be downloaded)
python extract_media.py ghost-export.json --dry-run

# Download all media
python extract_media.py ghost-export.json

# Custom output directory
python extract_media.py ghost-export.json --output my-media

# Different blog URL (for relative path resolution)
python extract_media.py ghost-export.json --blog-url https://myblog.com
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
