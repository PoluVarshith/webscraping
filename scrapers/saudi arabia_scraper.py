import urllib.request, json 
import tocsv
import pandas as pd
import twrv
import logfuns
import snowflake_queries
import scraper
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies
from time import sleep
"""
Spain website can only track one item
It needs 30 sec to load fully,  So wait implicitly_wait for 30
It only give Delivary time and data no location
"""
COUNTRY  = 'SAUDI ARABIA'
def change_date_format(date):
    #print(date)
    new_date = date.replace("-",'/')
    #print(new_date)
    return new_date

def change_time_format(time):
    #print(time)
    h,m,_ = time.split(":")
    new_time = ':'.join([h,m])
    #print(new_time)
    return new_time

def get_trackinginfo(tracking_info,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data):
    #tracking_num = 'CY364679371US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    tracking_num,facility_code = tracking_info
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    try:
        offset = list(config_data['OFFSET'][COUNTRY][str(facility_code)].values())
    except:
        offset = [0,0]
    try:
        proxy_details = config_data['PROXY_DETAILS']
        #print('proxy_details',proxy_details)
        username = proxy_details['username']
        password = proxy_details['password']
        endpoint = proxy_details['endpoint']
        port = proxy_details['port']
        #print('proxy_details',username,password,endpoint,port)
    except Exception as e:
        logger.info('proxy error:  '+str(e))

    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        url = urllib.request.urlopen(scraping_url)
        #url =  urllib.request.urlopen("https://splonline.com.sa/umbraco/api/tools/trackshipment?language=en&shipmentCode="
        #                            + str(tracking_num)) 
        data = json.load(url)
        #print(type(data))
        events  = data[0]['TrackingInfoItemList']
        #print('Number of events',len(events))
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        EventZipCode = []
        IsInHouse = []
        for i in events:
            if i['StatusMessage'] not in  ["",'null']:
                Track_nums.append(tracking_num)
                Codes.append('')
                Descs.append(i['StatusMessage'].strip())
                date,time = i['EventDateTime'].split('T')
                #print(date,time)
                Dates.append(change_date_format(date))
                new_time = change_time_format(time)
                Times.append(new_time)
                Locs.append(i['Office']+ " " + i['OfficeCode'])
                EventZipCode.append('')
                IsInHouse.append("FALSE")
        #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))

        df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs,EventZipCode,IsInHouse)        
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraped_tracking_nos.append(str(tracking_num))
        return df
    
    except Exception as e:
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        country_logger.info('Error: '+ str(e))
        if "NoneType" in str(e):
            discarded_tracking_nos.append(str(tracking_num))
        else:
            failed_tracking_nos.append(str(tracking_num))
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)

def scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    #print(len(tracking_nums))
    #tracking_info = tracking_info[0:1]
    batch_size = 20
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)
