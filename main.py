import scraper
import snowflake_queries
import twrv
from datetime import datetime,date
import os
import logging
import logfuns

    
def main():
    #countries = []
    log_dir_path = logfuns.make_logging_dir()
    #print(log_dir_path)
    #print(logfuns.make_logging_filepath(log_dir_path))

    logger = logfuns.set_logger(log_dir_path)
    logger.info("START TIMESTAMP :"+str(logfuns.get_date_time()))
    table = (snowflake_queries.get_config_table_data())
    logger.info('Config Table info\n' +str(table))
    threads =[]
    returns = []
    for c in table:
        country = c[0]
        query = c[1]
        if country == 'JAPAN':
            continue
        if country == 'JAPAN':
            scraping_url = 'https://trackings.post.japanpost.jp/services/srv/search/direct?reqCodeNo1=#TRACKING_NUM#&searchKind=S002&locale=en'
        else:
            scraping_url = "https://api1.correos.es/digital-services/searchengines/api/v1/?text=#TRACKING_NUM#&language=EN&searchType=envio"
        
        output_path = "\\\sauw1slprdsftp.file.core.windows.net\cornerstonesftp\FTPData\XPO\EPG\Prod\Tracking\Vendor\CommonVendor\sourcepath\\"
        #print(country,query)#,c[11],c[12])
        threads.append(twrv.ThreadWithReturnValue(target=scraper.scrape, args=(country,query,scraping_url,output_path,logger,log_dir_path)))

    for t in threads:
        t.start()

    for t in threads:
        returns.append(t.join())
    
def main_test():
    countries = ['SPAIN']
    for i in countries:
        scraper.scrape_test(i)

#main_test()
main()