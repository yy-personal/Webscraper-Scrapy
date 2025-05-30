# NCS Company Web Scraper

A Scrapy-based web scraping tool designed to extract content from the NCS company website (ncs.co). This tool crawls the website systematically, extracts text content, and saves it to a structured text file.

## Overview

This scraper is specifically configured to:
- Crawl the NCS company website (www.ncs.co)
- Extract page titles, headings (h1, h2), and paragraph text
- Respect rate limits and use polite crawling practices
- Rotate user agents to appear more like regular browser traffic
- Save all extracted content to a text file

## Features

- **Depth-limited crawling** (max 4 levels deep)
- **User agent rotation** for better success rates
- **Polite crawling** with delays between requests
- **Error handling** for common HTTP status codes
- **Domain restriction** to stay within ncs.co
- **Text file output** with structured formatting

## Prerequisites

Before running this scraper, ensure you have:

1. **Python 3.7+** installed on your system
2. **Scrapy framework** installed

### Installing Scrapy

```bash
pip install scrapy
```

Or if you're using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Scrapy
pip install scrapy
```

## Project Structure

```
company_scraper/
├── scrapy.cfg                 # Scrapy configuration file
└── company_scraper/
    ├── __init__.py
    ├── items.py              # Data models (currently empty)
    ├── middlewares.py        # Custom middleware (default)
    ├── pipelines.py          # Data processing pipelines
    ├── settings.py           # Scrapy settings
    └── spiders/
        └── company_spider.py # Main spider implementation
```

## How to Run

### Basic Usage

1. **Navigate to the project directory:**
   ```bash
   cd company_scraper
   ```

2. **Run the spider:**
   ```bash
   scrapy crawl ncs_web
   ```

### Advanced Usage

**Run with custom settings:**
```bash
# Increase verbosity for debugging
scrapy crawl ncs_web -L DEBUG

# Limit to specific number of pages
scrapy crawl ncs_web -s CLOSESPIDER_PAGECOUNT=50

# Change output file name by modifying the pipeline
# (requires code modification in pipelines.py)
```

**Run with custom depth limit:**
```bash
scrapy crawl ncs_web -s DEPTH_LIMIT=2
```

## Configuration Options

The spider includes several configurable settings in `company_spider.py`:

### Crawling Behavior
- **DEPTH_LIMIT**: `4` - Maximum crawl depth
- **DOWNLOAD_DELAY**: `1` - Base delay between requests (seconds)
- **RANDOMIZE_DOWNLOAD_DELAY**: `1` - Adds randomization to delays
- **CONCURRENT_REQUESTS**: `2` - Number of concurrent requests

### Domains and URLs
- **Start URL**: `https://www.ncs.co/`
- **Allowed domains**: `["www.ncs.co", "ncs.co"]`

### User Agents
The spider rotates between multiple realistic user agents to avoid detection:
- Chrome (Windows/Mac/Linux)
- Firefox
- Safari
- Edge

## Output

### File Output
The scraper generates a text file named `ncs_web_data.txt` with the following format:

```
COMPANY WEBSITE SCRAPE RESULTS
============================

URL: https://www.ncs.co/
TITLE: [Page Title]
DEPTH: 0
CONTENT:
[Extracted text content from title, headings, and paragraphs]

--------------------------------------------------------------------------------

URL: https://www.ncs.co/about-us
TITLE: [Page Title]
DEPTH: 1
CONTENT:
[Extracted text content]

--------------------------------------------------------------------------------

Total pages scraped: [Number]
```

### Console Output
During execution, you'll see:
- URLs being processed
- HTTP status codes
- Any warnings or errors
- Final statistics

## Error Handling

The spider handles common issues:

- **403 Forbidden**: Logs warning about potential blocking
- **404 Not Found**: Logs warning and continues
- **500/503 Server Errors**: Retries up to 3 times
- **Timeouts**: Automatic retry mechanism

## Customization

### Modifying Target Website
To scrape a different website, update these values in `company_spider.py`:

```python
start_urls = ["https://your-target-site.com/"]
allowed_domains = ["your-target-site.com"]
```

### Changing Output Format
To modify the output, edit the `TextWriterPipeline` class in `pipelines.py`:

```python
def process_item(self, item, spider):
    # Customize how data is written to file
    self.file.write(f"Custom format: {item['title']}\n")
    return item
```

### Adding More Data Extraction
Enhance the `parse` method in `company_spider.py` to extract additional elements:

```python
# Extract additional elements
page_links = response.css('a::attr(href)').getall()
page_images = response.css('img::attr(src)').getall()

# Add to yield statement
yield {
    'url': current_url,
    'title': page_title,
    'content': all_text,
    'links': page_links,
    'images': page_images,
    # ... other fields
}
```

## Troubleshooting

### Common Issues

**1. "No module named 'scrapy'"**
```bash
pip install scrapy
```

**2. "Spider not found"**
Ensure you're in the correct directory (`company_scraper/`) and the spider name is correct (`ncs_web`).

**3. "403 Forbidden" responses**
The website may be blocking requests. Try:
- Increasing delays: `-s DOWNLOAD_DELAY=3`
- Reducing concurrency: `-s CONCURRENT_REQUESTS=1`

**4. No output file generated**
Check that the `TextWriterPipeline` is enabled in `settings.py`:
```python
ITEM_PIPELINES = {
    'company_scraper.pipelines.TextWriterPipeline': 300,
}
```

### Debug Mode
Run with debug logging to see detailed information:
```bash
scrapy crawl ncs_web -L DEBUG
```

## Legal and Ethical Considerations

- **Robots.txt**: Currently set to `ROBOTSTXT_OBEY = False` - consider changing to `True` for compliance
- **Rate limiting**: The spider includes delays to be respectful of the target server
- **Terms of service**: Ensure your usage complies with the website's terms of service
- **Data usage**: Only use scraped data in accordance with applicable laws and regulations

## Support

For issues with:
- **Scrapy framework**: Visit [Scrapy documentation](https://docs.scrapy.org/)
- **This specific scraper**: Check the troubleshooting section above or review the spider logs

## License

This tool is provided as-is for educational and research purposes. Ensure compliance with all applicable laws and website terms of service when using.