import snowflake_queries
import time

def scrape(country):
    trackingnums_query = snowflake_queries.get_trackingnums_query(country)
    tracking_nums = snowflake_queries.get_tracknums(trackingnums_query)
    print(len(tracking_nums))
    scraper_name = country.lower() + '_scraper'
    imported = getattr(__import__('scrapers', fromlist=[scraper_name]),scraper_name)
    
