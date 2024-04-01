import urllib.request, json 
import tocsv
import pandas as pd
import twrv
import logfuns
import snowflake_queries
import scraper
"""
Spain website can only track one item
It needs 30 sec to load fully,  So wait implicitly_wait for 30
It only give Delivary time and data no location
"""
COUNTRY  = 'SPAIN'
def change_date_format(date):
    d,m,y = date.split('/')
    new_date = '/'.join([y,m,d])
    #print(new_date)
    return new_date

def get_trackinginfo(tracking_num,scraping_tracking_nos,scraping_url,country_logger,log_country_dir_path=None):
    #tracking_num = 'CY139861975US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('SCRAPING STARTED FOR TRACKING NUMBER: ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scarping_url)
        url = urllib.request.urlopen(scraping_url)
        #url =  urllib.request.urlopen("https://api1.correos.es/digital-services/searchengines/api/v1/?text=" 
        #                            + str(tracking_num) + "&language=EN&searchType=envio") 
        data = json.load(url)
        #print(type(data))
        country_logger.info('URL QUERY SUCCESSFUL FOR TRACKING NUMBER: ' + str(tracking_num))
        events  = data['shipment'][0]['events']
        #print(len(events))
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        EventZipCode = []
        IsInHouse = []
        for i in events:
            if i['extendedText'] not in  ["",'null']:
                Track_nums.append(tracking_num)
                Codes.append('')
                Descs.append(i['extendedText'])
                new_date = change_date_format(i['eventDate'])
                Dates.append(new_date)
                h,m,s = i['eventTime'].split(":")
                new_time = ":".join([h,m])
                Times.append(new_time)
                Locs.append("")
                EventZipCode.append('')
                IsInHouse.append("FALSE")
        #print(len(Track_nums),len(Descs))
        
        country_logger.info('INFO SCRAPING SUCCESSFUL FOR TRACKING NUMBER: ' + str(tracking_num))
        df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs,EventZipCode,IsInHouse)
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraping_tracking_nos.append(str(tracking_num))
        return df
    except Exception as e:
        country_logger.info(str(tracking_num) +' scraping failed due to error below, Scraping_URL: ' + str(scraping_url))
        country_logger.info('Scraping Error for Tracking Number '+ str(tracking_num)+' :' + str(e))
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)

def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id):
    #tracking_nums = tracking_nums[0:1]
    batch_size = 20
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id)
