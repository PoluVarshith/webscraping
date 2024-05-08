import urllib.request, json 
import tocsv
import pandas as pd
import twrv
from deep_translator import GoogleTranslator
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logfuns
import scraper

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies
from time import sleep

username = 'brd-customer-hl_5d2a07b1-zone-scraping_proxy'
password = '4m9u2j5nl598'
endpoint = 'brd.superproxy.io'
port = '22225'

COUNTRY = 'FRANCE'
def change_date_format(date):
    #print(date)
    new_date = date.replace("-",'/')
    #print(new_date)
    return new_date

def change_time_format(time):
    #print(time)
    a,_ = time.split('+')
    h,m,_ = a.split(":")
    new_time = ':'.join([h,m])
    #print(new_time)
    return new_time

def get_trackinginfo(tracking_info,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data):
    #tracking_num ='CY140541041US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    tracking_num,facility_code = tracking_info
    try:
        offset = list(config_data['OFFSET'][COUNTRY][str(facility_code)].values())
    except:
        offset = [0,0]
        
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        
        chrome_options = webdriver.ChromeOptions()
        proxies_extension = proxies(username, password, endpoint, port)

        chrome_options.add_extension(proxies_extension)
        #chrome_options.add_argument("--headless=new")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(scraping_url)
        #print(scraping_url)
        #scraping_url = "https://www.laposte.fr/ssu/sun/back/suivi-unifie/#TRACKING_NUM#?lang=en_GB"
        #url = ('https://www.deutschepost.de/int-verfolgen/data/search?piececode=' + str(tracking_num) + '&inputSearch=true&language=en')
        
        #driver.get(scraping_url)
        driver.implicitly_wait(50)
        sleep(5)
        #print(driver.page_source)
        data = driver.find_element(By.TAG_NAME,'body').text
        #print('hello',type(data),data)
        data = json.loads(data)
        #print(type(data))
        try :
            events = data[0]['shipment']['event']
        except Exception as e:
            country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
            country_logger.info(str(tracking_num) +' Error : "no data available?  ' + str(scraping_url))
            discarded_tracking_nos.append(str(tracking_num))
            return tocsv.emtpy_frame()
        #print(len(events))
        #print(events)
        driver.close()
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        EventZipCode = []
        IsInHouse = []
        for i in events:
            Track_nums.append(tracking_num)
            Codes.append('')
            Descs.append(i['label'])
            date,time = i['date'].split('T')
            #print(date,time)
            new_date = change_date_format(date)
            Dates.append(new_date)
            new_time = change_time_format(time)
            Times.append(new_time)
            Locs.append('')
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
        #if "Unable to locate element" in str(e):
        failed_tracking_nos.append(str(tracking_num))
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)
    
def scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    #print(len(tracking_nums))
    tracking_info = tracking_info[:3]
    batch_size = 5
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)

