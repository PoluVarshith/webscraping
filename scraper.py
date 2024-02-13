import snowflake_queries
import time

def scrape(country,trackingnums_query,scraping_url,output_path,logger,log_dir_path,c_audit):
    tracking_nums = [str(i[0]) for i in snowflake_queries.get_tracknums(trackingnums_query)]
    logger.info(str(country) + ' Total Tracking Numbers :' + str(len(tracking_nums)))
    logger.info(str(tracking_nums))
    c_audit['ACTUAL_TRACKING_NOS'] = tracking_nums
    scraper_name = country.lower() + '_scraper'
    scrape_country = getattr(__import__('scrapers', fromlist=[scraper_name]),scraper_name)
    scrape_country.scrape_list(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit)
