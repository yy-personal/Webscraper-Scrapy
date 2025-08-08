# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Scrapy-based web scraper designed to extract content from the NCS company website (ncs.co). The spider crawls systematically, extracts text content from titles, headings, and paragraphs, and saves it to a structured text file.

## Commands

### Running the Scraper
```bash
cd company_scraper
scrapy crawl ncs_web
```

### Debug Mode
```bash
scrapy crawl ncs_web -L DEBUG
```

### Custom Settings
```bash
# Limit pages scraped
scrapy crawl ncs_web -s CLOSESPIDER_PAGECOUNT=50

# Change depth limit
scrapy crawl ncs_web -s DEPTH_LIMIT=2

# Adjust delays for politeness
scrapy crawl ncs_web -s DOWNLOAD_DELAY=3 -s CONCURRENT_REQUESTS=1
```

### Dependencies
Only requires Scrapy framework:
```bash
pip install scrapy
```

## Architecture

### Core Components

- **Spider**: `company_scraper/spiders/company_spider.py` (CompanySpider class, name="ncs_web")
  - Handles crawling logic with depth limit of 4 levels
  - Uses user agent rotation and polite crawling (1-2 second delays)
  - Extracts titles, h1/h2 headings, and paragraphs
  - Respects domain boundaries (ncs.co only)

- **Pipeline**: `company_scraper/pipelines.py` (TextWriterPipeline)
  - Writes scraped content to `ncs_web_data.txt` in structured format
  - Enabled in settings.py with priority 300

- **Settings**: `company_scraper/settings.py`
  - ROBOTSTXT_OBEY=True (default configuration)
  - TextWriterPipeline enabled
  - UTF-8 encoding configured

### Spider Configuration

The spider uses custom_settings in `company_spider.py:21-52` that override global settings:
- ROBOTSTXT_OBEY=False (overrides global setting)
- Depth limit, delays, concurrent requests, error handling
- User agent rotation with realistic browser headers
- Retry logic for common HTTP errors (403, 404, 500, 503)

### Data Flow

1. Spider starts at https://www.ncs.co/
2. Extracts page content (title, headings, paragraphs)
3. Follows internal links up to depth 4
4. TextWriterPipeline processes each item and writes to text file
5. Final output includes total page count

### Output Format

Text file (`ncs_web_data.txt`) with structure:
```
URL: [page_url]
TITLE: [page_title]  
DEPTH: [crawl_depth]
CONTENT: [extracted_text]
```

## Key Features

- User agent rotation to mimic different browsers
- Polite crawling with delays and concurrent request limits
- HTTP error handling and retry logic
- Domain restriction to prevent crawling external sites
- Depth-limited crawling to control scope
- Structured text output with metadata