import scraper
import snowflake_queries
import twrv
from datetime import datetime,date
import os
import logging
import logfuns
import yaml

config_data = []
def main():
    with open('config.yaml','r') as config:
        config_data = yaml.safe_load(config)
        #print(config_data)
        connection_details = config_data[config_data['ENV']]
        snowflake_queries.connection_details = connection_details
        
    log_dir_path,output_dir_path = logfuns.make_logging_dir(config_data['LOG_PATH'])
    snowflake_queries.session_log_path = log_dir_path
    logger = logfuns.set_logger(log_dir_path)
    logger.info("START TIMESTAMP :"+str(logfuns.get_date_time()))
    table = (snowflake_queries.get_config_table_data())
    #logger.info('Config Table info\n' +str(table))
    threads =[]
    returns = []
    prev_run_id = snowflake_queries.get_prev_run_id()
    cur_run_id = prev_run_id + 1
    logger.info("The current run id is :"+str(cur_run_id))
    for c in table:
        postal_site_id,country,query,scraping_url,output_path = c  
        logger.info("\n Running Country Config table entry:"+str(postal_site_id)+"\n country:"+str(country)+"\n scraping_url:"+str(scraping_url)+"\n output path:"+str(output_path))
        snowflake_queries.postal_ids_to_countries[postal_site_id] = country
        #output_path = output_dir_path  #######IN LOCAL#######      
        c_audit = {}
        c_audit['POSTAL_SITE_ID'] = postal_site_id
        threads.append(twrv.ThreadWithReturnValue(target=scraper.scrape_country, args=(country,query,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)))

    for t in threads:
        t.start()

    for t in threads:
        returns.append(t.join())

    snowflake_queries.check_audit_status(cur_run_id,config_data)

main()

"""
UW1PRDEPGRDS04
UW1PRDEPGRDS05
UW1PRDEPGRDS06

Test - UW1TSTEPGAPP07
Stage - UW1STGEPGAPP07
Prod - UW1PRDEPGAPP07
"""

