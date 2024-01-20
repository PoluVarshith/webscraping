import snowflake_queries
import time

def scrape(country):
    trackingnums_query = snowflake_queries.get_trackingnums_query(country)
    tracking_nums = snowflake_queries.get_tracknums(trackingnums_query)
    print('Total Tracking Numbers :',len(tracking_nums))
    scraper_name = country.lower() + '_scraper'
    scrape_country = getattr(__import__('scrapers', fromlist=[scraper_name]),scraper_name)
    scrape_country.scrape_list(tracking_nums)
