import scraper
import snowflake_queries
import twrv
from datetime import datetime,date
import os
import logging
import logfuns

    
def main():
    log_dir_path,output_dir_path = logfuns.make_logging_dir()
    logger = logfuns.set_logger(log_dir_path)
    logger.info("START TIMESTAMP :"+str(logfuns.get_date_time()))
    table = (snowflake_queries.get_config_table_data())
    logger.info('Config Table info\n' +str(table))
    threads =[]
    returns = []
    prev_run_id = snowflake_queries.get_prev_run_id()
    cur_run_id = prev_run_id + 1
    for c in table:
        postal_side_id,country,query,scraping_url,output_path = c  
        #output_path = output_dir_path  #######IN LOCAL#######      
        c_audit = {}
        c_audit['POSTAL_SITE_ID'] = postal_side_id
        threads.append(twrv.ThreadWithReturnValue(target=scraper.scrape_country, args=(country,query,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id)))

    for t in threads:
        t.start()

    for t in threads:
        returns.append(t.join())

    #snowflake_queries.check_audit_status(cur_run_id)
    #logfuns.send_audit_notification()
main()

"""
UW1PRDEPGRDS04
UW1PRDEPGRDS05
UW1PRDEPGRDS06

Test - UW1TSTEPGAPP07
Stage - UW1STGEPGAPP07
Prod - UW1PRDEPGAPP07
"""

"""
YAML CONFIG
snowflake connection details
env name
mail details
log path
"""