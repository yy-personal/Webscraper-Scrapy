# Define your item pipelines here
#
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter

class CompanyScraperPipeline:
    def process_item(self, item, spider):
        return item

class TextWriterPipeline:
    def __init__(self):
        self.files = {}  # Dictionary to hold file handles for each region
        self.region_stats = {}  # Track stats per region
        self.region_filenames = {
            'Singapore': 'ncs_web_sg.txt',
            'China': 'ncs_web_cn.txt',
            'India': 'ncs_web_in.txt',
            'Australia': 'ncs_web_au.txt'
        }
    
    def open_spider(self, spider):
        # Open separate files for each region
        for region, filename in self.region_filenames.items():
            self.files[region] = open(filename, 'w', encoding='utf-8')
            # Write headers to each file
            self.files[region].write(f"NCS {region.upper()} WEBSITE SCRAPE RESULTS\n")
            self.files[region].write("=" * (len(f"NCS {region.upper()} WEBSITE SCRAPE RESULTS")) + "\n\n")
    
    def close_spider(self, spider):
        # Close all files and write summaries
        for region, file_handle in self.files.items():
            if file_handle:
                file_handle.write(f"\n{'='*80}\n")
                file_handle.write("SCRAPE SUMMARY\n")
                file_handle.write(f"{'='*80}\n")
                pages_count = self.region_stats.get(region, 0)
                file_handle.write(f"Total pages scraped for {region}: {pages_count}\n")
                file_handle.close()
    
    def process_item(self, item, spider):
        # Track region statistics
        region = item.get('region', 'Unknown')
        self.region_stats[region] = self.region_stats.get(region, 0) + 1
        
        # Write to the appropriate regional file
        if region in self.files:
            file_handle = self.files[region]
            file_handle.write(f"URL: {item['url']}\n")
            file_handle.write(f"TITLE: {item['title']}\n")
            file_handle.write(f"DEPTH: {item['depth']}\n")
            file_handle.write("CONTENT:\n")
            file_handle.write(f"{item['content']}\n")
            file_handle.write("\n" + "-"*80 + "\n\n")  # Separator between items
        else:
            # Handle unknown regions by logging a warning
            spider.logger.warning(f"Unknown region: {region} for URL: {item['url']}")
            
        return item