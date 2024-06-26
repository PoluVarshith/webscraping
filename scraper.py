import time
import logfuns
import twrv
import tocsv
import snowflake_queries

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def scrape_country(country,trackingnums_query,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    tracking_info  = snowflake_queries.get_tracknums(trackingnums_query)
    #print("info",tracking_info,len(tracking_info),type(tracking_info[0]))
    logger.info(str(country) + ' Total Tracking Numbers :' + str(len(tracking_info)))
    logger.info(str(tracking_info))
    scraper_name = country.lower() + '_scraper'
    scrape_country = getattr(__import__('scrapers', fromlist=[scraper_name]),scraper_name)
    scrape_country.scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)

def scrape_batch(COUNTRY,TRACKIN_FUNC,tracking_info_batch,scraping_url,output_path,country_logger,log_country_dir_path,c_audit,dfs,scraping_tracking_nos,discarded_tracking_nos,failed_tracking_nos,config_data):
    #print(COUNTRY)
    country_logger.info("Total Tracking Numbers in this batch: " + str(len(tracking_info_batch)))
    country_logger.info('List of Tracking Numbers in this batch: ' + str(tracking_info_batch))
    
    threads =[]
    for i in tracking_info_batch:
        threads.append(twrv.ThreadWithReturnValue(target=TRACKIN_FUNC, args=(i,scraping_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data,)))
    
    for t in threads:
        t.start()

    for t in threads:
        dfs.append(t.join())


def scrape_list(COUNTRY,TRACKIN_FUNC,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    c_audit['RUN_ID'] = str(cur_run_id)
    c_audit['START_DATETIME'] = logfuns.get_date_time_normal_format()
    c_audit['ACTUAL_TRACKING_NOS'] = tracking_info
    country_logger = logfuns.set_logger(log_dir_path,country=COUNTRY)
    country_logger.info("Total Tracking Numbers :" + str(len(tracking_info)))
    country_logger.info('List of Tracking Numbers ' + str(tracking_info))
    log_country_dir_path = logfuns.make_logging_country_dir(COUNTRY,log_dir_path)
    scraped_tracking_nos = []
    discarded_tracking_nos = []
    failed_tracking_nos = []
    dfs = []
    for i in chunks(tracking_info,batch_size):
        scrape_batch(COUNTRY,TRACKIN_FUNC,i,scraping_url,output_path,country_logger,log_country_dir_path,c_audit,dfs,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,config_data)
    
    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv(output_path,output_dir_path,country_logger)
    c_audit['END_DATETIME'] = logfuns.get_date_time_normal_format()
    c_audit['SCRAPED_TRACKING_NOS'] = scraped_tracking_nos
    c_audit['DISCARDED_TRACKING_NOS'] = discarded_tracking_nos
    c_audit['FAILED_TRACKING_NOS'] = failed_tracking_nos
    c_audit['STATUS'] = 'COMPLETED' if len(failed_tracking_nos) == 0  == 0 else 'FAILED'
    #c_audit['STATUS'] = 'COMPLETED' if len(list(set(new_list) - set(c_audit['SCRAPED_TRACKING_NOS']))) == 0 else 'FAILED'
    country_logger.info('AUDIT INFO : '+ str(c_audit))
    #print(len(scraped_tracking_nos),len(discarded_tracking_nos),len(failed_tracking_nos))
    country_logger.info('Total Scraped Tracking Numbers : '+ str(len(scraped_tracking_nos)))
    country_logger.info('Total Discarded Tracking Numbers : '+ str(len(discarded_tracking_nos)))
    country_logger.info('Total Failed Tracking Numbers : '+ str(len(failed_tracking_nos)))
    snowflake_queries.insert_audit_info(c_audit,country_logger)