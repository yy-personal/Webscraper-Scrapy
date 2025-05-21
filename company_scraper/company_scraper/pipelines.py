# Define your item pipelines here
#
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter

class CompanyScraperPipeline:
    def process_item(self, item, spider):
        return item

class TextWriterPipeline:
    def __init__(self):
        self.file = None
    
    def open_spider(self, spider):
        # Open the text file for writing when the spider starts
        self.file = open('ncs_web_data.txt', 'w', encoding='utf-8')
        # Write a header to the file
        self.file.write("COMPANY WEBSITE SCRAPE RESULTS\n")
        self.file.write("============================\n\n")
    
    def close_spider(self, spider):
        # Close the file when the spider finishes
        if self.file:
            self.file.write(f"\nTotal pages scraped: {len(spider.visited_urls)}\n")
            self.file.close()
    
    def process_item(self, item, spider):
        # Write each scraped item to the text file
        self.file.write(f"URL: {item['url']}\n")
        self.file.write(f"TITLE: {item['title']}\n")
        self.file.write(f"DEPTH: {item['depth']}\n")
        self.file.write("CONTENT:\n")
        self.file.write(f"{item['content']}\n")
        self.file.write("\n" + "-"*80 + "\n\n")  # Separator between items
        return item