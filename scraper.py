import time
import logfuns
import twrv
import tocsv
import snowflake_queries

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def scrape_country(country,trackingnums_query,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id):
    tracking_nums = [str(i[0]) for i in snowflake_queries.get_tracknums(trackingnums_query)]
    logger.info(str(country) + ' Total Tracking Numbers :' + str(len(tracking_nums)))
    logger.info(str(tracking_nums))
    scraper_name = country.lower() + '_scraper'
    scrape_country = getattr(__import__('scrapers', fromlist=[scraper_name]),scraper_name)
    scrape_country.scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id)

def scrape_batch(COUNTRY,TRACKIN_FUNC,tracking_nums_batch,scraping_url,output_path,country_logger,log_country_dir_path,c_audit,dfs,scraping_tracking_nos,discarded_tracking_nos):
    #print(COUNTRY)
    country_logger.info("Total Tracking Numbers in this batch: " + str(len(tracking_nums_batch)))
    country_logger.info('List of Tracking Numbers in this batch: ' + str(tracking_nums_batch))
    
    threads =[]
    for i in tracking_nums_batch:
        threads.append(twrv.ThreadWithReturnValue(target=TRACKIN_FUNC, args=(i,scraping_tracking_nos,discarded_tracking_nos,scraping_url,country_logger,log_country_dir_path,)))
    
    for t in threads:
        t.start()

    for t in threads:
        dfs.append(t.join())


def scrape_list(COUNTRY,TRACKIN_FUNC,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id):
    c_audit['RUN_ID'] = str(cur_run_id)
    c_audit['START_DATETIME'] = logfuns.get_date_time_normal_format()
    c_audit['ACTUAL_TRACKING_NOS'] = tracking_nums
    country_logger = logfuns.set_logger(log_dir_path,country=COUNTRY)
    country_logger.info("Total Tracking Numbers :" + str(len(tracking_nums)))
    country_logger.info('List of Tracking Numbers ' + str(tracking_nums))
    log_country_dir_path = logfuns.make_logging_country_dir(COUNTRY,log_dir_path)
    scraped_tracking_nos = []
    discarded_tracking_nos = []
    dfs = []
    for i in chunks(tracking_nums,batch_size):
        scrape_batch(COUNTRY,TRACKIN_FUNC,i,scraping_url,output_path,country_logger,log_country_dir_path,c_audit,dfs,scraped_tracking_nos,discarded_tracking_nos)
    
    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv(output_path,output_dir_path,country_logger)
    c_audit['END_DATETIME'] = logfuns.get_date_time_normal_format()
    c_audit['SCRAPED_TRACKING_NOS'] = scraped_tracking_nos
    c_audit['DISCARDED_TRACKING_NOS'] = discarded_tracking_nos
    new_list = tracking_nums
    for d in discarded_tracking_nos:
        new_list.remove(d)
    c_audit['STATUS'] = 'COMPLETED' if len(list(set(new_list) - set(c_audit['SCRAPED_TRACKING_NOS']))) == 0 else 'FAILED'
    country_logger.info('AUDIT INFO : '+ str(c_audit))
    snowflake_queries.insert_audit_info(c_audit,country_logger)