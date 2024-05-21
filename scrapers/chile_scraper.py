from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator
import tocsv
import pandas as pd
import twrv
import scraper
import logfuns
from time import sleep
from time import sleep
from threading import Thread
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies

COUNTRY = 'CHILE'



def change_date_format(date):
    #print(date)
    mm,dd,yyyy = date.split("/")
    dd = "%02d" % int(dd)
    mm = "%02d" % int(mm)
    new_date = "/".join([yyyy,mm,dd])
    #print(new_date)
    return new_date

def change_time_format(time,format):
    #print(time)
    hr,mn,sec = time.split(":")
    h = int(hr)
    if format == 'PM':
        if h != 12:
            h = int(h)+12
    elif format == 'AM':
        if h ==12:
            h = 0
    h = "%02d" % h
    new_time = ':'.join([h,mn])
    #print(new_time)
    return new_time

def get_trackinginfo(tracking_info,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data):
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    tracking_num,facility_code = tracking_info
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #tracking_num = 'CY363928611US'
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
        driver.quit()
        country_logger.info('End of Scraping for : '+ str(tracking_num))
        logger.info('proxy error:  '+str(e))


    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        #print(tracking_num)
        options = Options()
        #options.add_argument('--headless=new')
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )
        """chrome_options = webdriver.ChromeOptions()
        proxies_extension = proxies(username, password, endpoint, port)

        chrome_options.add_extension(proxies_extension)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)"""

        #driver.get('https://service.post.ch/ekp-web/ui/entry/search/' + str(tracking_num))
        driver.get(scraping_url)
        driver.implicitly_wait(15)
        button = driver.find_element(By.CLASS_NAME,'more-btn')
        button.click()
        translate = driver.find_element(By.CLASS_NAME,'translate')
        translate =translate.find_element(By.TAG_NAME,'label')
        translate.click()
        sleep(5)
            
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        EventZipCode=[]
        IsInHouse = []
        list = driver.find_element(By.CLASS_NAME,'tracking-list-package-content')
        list = list.find_elements(By.TAG_NAME,'ul')

        USPS_TABLE = list[1].find_elements(By.TAG_NAME,'li')
        #print(len(USPS_TABLE))
        usps_dates = []
        usps_times = []
        for t in USPS_TABLE:
            date_time = t.find_element(By.TAG_NAME,'time').text
            #print(date_time)
            date, time , format = date_time.split(" ")
            new_time = change_time_format(time,format)
            new_date = change_date_format(date)
            usps_dates.append(new_date)
            usps_times.append(new_time)
        #print(usps_dates,usps_times)
        CHILE_TABLE = list[0].find_elements(By.TAG_NAME,'li')
        #print(len(CHILE_TABLE))

        for t in CHILE_TABLE:
            date_time = t.find_element(By.TAG_NAME,'time').text
            date, time , format = date_time.split(" ")
            new_time = change_time_format(time,format)
            new_date = change_date_format(date)
            if new_time in usps_times and new_date in usps_dates:
                continue
            desc = t.find_element(By.CLASS_NAME,'info').text
            desc_tok = desc.split(".")
            desc = desc_tok[0]
            loc = ".".join(desc_tok[1:])
            #print(new_date,new_time,format,desc,'******',loc)
        
            Dates.append(new_date)
            Times.append(new_time)
            Track_nums.append(tracking_num)
            Codes.append('')
            #print('datetime',new_date,time)
            Descs.append(desc)
            Locs.append(loc)
            EventZipCode.append('')
            IsInHouse.append("FALSE")
            #print('descloc',desc,loc)
        #print(Dates,Times)
        driver.quit()
        country_logger.info('End of Scraping for : '+ str(tracking_num))

        #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))
        df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs,EventZipCode,IsInHouse)        
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraped_tracking_nos.append(str(tracking_num))
        return df

    except Exception as e:
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        country_logger.info('Error: '+ str(e))
        if "Unable to locate element" in str(e):
            discarded_tracking_nos.append(str(tracking_num))
        else:
            failed_tracking_nos.append(str(tracking_num))
        driver.quit()
        country_logger.info('End of Scraping for : '+ str(tracking_num))
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)
def scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    #tracking_info = tracking_info[:4]
    batch_size = 4
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)
