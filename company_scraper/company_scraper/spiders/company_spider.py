import scrapy
import random
from urllib.parse import urlparse

class CompanySpider(scrapy.Spider):
    name = "ncs_web"
    start_urls = ["https://www.ncs.co/"]
    allowed_domains = ["www.ncs.co", "ncs.co"]
    visited_urls = set()
    
    # List of different user agents to rotate through
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/131.0.0.0 Safari/537.36',
    ]
    
    custom_settings = {
        'DEPTH_LIMIT': 4,
        'DOWNLOAD_DELAY': 1,  # Increased delay
        'RANDOMIZE_DOWNLOAD_DELAY': 1,  # Random delay between 2-4 seconds
        'ROBOTSTXT_OBEY': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        
        # Handle HTTP errors
        'HTTPERROR_ALLOWED_CODES': [403, 404, 500, 503],
        
        # More realistic browser headers
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        },
        
        # Retry settings
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429, 403],
        
        # Concurrent requests (lower to be more polite)
        'CONCURRENT_REQUESTS': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
    }

    def get_random_user_agent(self):
        """Return a random user agent from the list"""
        return random.choice(self.user_agents)

    def start_requests(self):
        """Override start_requests to add rotating user agent"""
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers={
                    'User-Agent': self.get_random_user_agent(),
                    'Referer': 'https://www.google.com/',  # Pretend we came from Google
                }
            )

    def parse(self, response):
        current_url = response.url
        
        # Log the status for debugging
        self.logger.info(f"Status {response.status} for {current_url}")
        
        # Handle different status codes
        if response.status == 403:
            self.logger.warning(f"403 Forbidden for {current_url}. The site might be blocking us.")
            return
        
        if response.status in [404, 500, 503]:
            self.logger.warning(f"HTTP {response.status} for {current_url}")
            return
        
        if current_url in self.visited_urls:
            return
        
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
            'depth': response.meta.get('depth', 0),
            'status': response.status
        }
        
        # Find all links on the page
        links = response.css('a::attr(href)').getall()
        
        # Follow links within the same domain
        for link in links:
            next_page = response.urljoin(link)
            parsed_url = urlparse(next_page)
            
            if parsed_url.netloc in self.allowed_domains:
                yield scrapy.Request(
                    next_page, 
                    callback=self.parse,
                    meta={'depth': response.meta.get('depth', 0) + 1},
                    headers={
                        'User-Agent': self.get_random_user_agent(),
                        'Referer': current_url,
                    }
                )