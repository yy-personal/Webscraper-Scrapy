# Step 1: Install Scrapy
# Run in command line: pip install scrapy

# Step 2: Create a new Scrapy project
# Run in command line: scrapy startproject company_scraper
# cd company_scraper

# Step 3: Create a spider file in the spiders directory
# File: company_scraper/company_scraper/spiders/company_spider.py

import scrapy
from urllib.parse import urlparse

class CompanySpider(scrapy.Spider):
    name = "ncs_web"
    # Replace with your company's website URL
    start_urls = ["https://www.ncs.co/"]
    
    # Set the allowed domains to restrict crawling to your company website
    allowed_domains = ["www.ncs.co"]
    
    # Track visited URLs to avoid duplicates
    visited_urls = set()
    
    # Configure settings directly in the spider
    custom_settings = {
        'DEPTH_LIMIT': 4,  # Set crawl depth (adjust as needed)
        'DOWNLOAD_DELAY': 1,  # Be respectful with 1 second delay between requests
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False,  # Respect robots.txt rules
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        # Extract current page URL
        current_url = response.url
        
        # Skip if we've already visited this URL
        if current_url in self.visited_urls:
            return
        
        # Add URL to visited set
        self.visited_urls.add(current_url)
        
        # Extract page data
        page_title = response.css('title::text').get()
        page_h1 = response.css('h1::text').getall()
        page_h2 = response.css('h2::text').getall()
        page_paragraphs = response.css('p::text').getall()
        
        # Clean and join text data
        all_text = ' '.join([
            page_title or '',
            ' '.join(page_h1 or []),
            ' '.join(page_h2 or []),
            ' '.join(page_paragraphs or [])
        ]).strip()
        
        # Store the data
        yield {
            'url': current_url,
            'title': page_title,
            'content': all_text,
            'depth': response.meta.get('depth', 0)
        }
        
        # Find all links on the page
        links = response.css('a::attr(href)').getall()
        
        # Follow links within the same domain
        for link in links:
            # Convert relative URLs to absolute URLs
            next_page = response.urljoin(link)
            
            # Make sure we stay within our domain
            parsed_url = urlparse(next_page)
            if parsed_url.netloc in self.allowed_domains:
                yield scrapy.Request(
                    next_page, 
                    callback=self.parse,
                    meta={'depth': response.meta.get('depth', 0) + 1}
                )

# Step 4: Run the spider and save results
# Run in command line: 
# scrapy crawl company -o company_data.json