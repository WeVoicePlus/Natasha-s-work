import os
from icrawler.builtin import BingImageCrawler

def crawl_bing(save_path, keyword, max_num=250):
    bing_crawler = BingImageCrawler(downloader_threads=4,
                    storage={'root_dir': save_path})
    bing_crawler.crawl(keyword=keyword, filters=None, offset=0, max_num=max_num)

if __name__ == "__main__":
    keywords = ["hong kong delivery motorcycle"]
    for kw in keywords:
        crawl_bing(os.path.join("imgs",kw), kw, max_num=100)
    