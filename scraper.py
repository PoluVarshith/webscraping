import snowflake_queries
import time

def scrape(country,trackingnums_query,scraping_url,output_path,logger,log_dir_path):
    tracking_nums = snowflake_queries.get_tracknums(trackingnums_query)
    logger.info(str(country) + ' Total Tracking Numbers :' + str(len(tracking_nums)))
    logger.info(str(tracking_nums))
    scraper_name = country.lower() + '_scraper'
    scrape_country = getattr(__import__('scrapers', fromlist=[scraper_name]),scraper_name)
    scrape_country.scrape_list(tracking_nums,scraping_url,output_path,logger,log_dir_path)

def scrape_test(country):
    print('test scraper')
    trackingnums_query = snowflake_queries.get_trackingnums_query(country)
    tracking_nums = snowflake_queries.get_tracknums(trackingnums_query)
    print(country,'Total Tracking Numbers :',len(tracking_nums))
    print(tracking_nums)
    scraper_name = country.lower() + '_scraper'
    scrape_country = getattr(__import__('scrapers', fromlist=[scraper_name]),scraper_name)
    scrape_country.scrape_list(tracking_nums)