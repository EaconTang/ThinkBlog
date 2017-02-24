import pysitemap
import os


def main():
    sitemap_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sitemap.xml')
    crawler = pysitemap.Crawler(url='http://blog.tangyingkang.com/',
                                outputfile=sitemap_file,
                                logfile='/var/log/sitemap.log',
                                oformat='xml')
    crawler.crawl()


if __name__ == '__main__':
    main()
