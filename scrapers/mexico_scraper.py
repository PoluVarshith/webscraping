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


COUNTRY = 'MEXICO'

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
    tracking_num = 'CY363884990US'
    try:
        offset = list(config_data['OFFSET'][COUNTRY][str(facility_code)].values())
    except:
        offset = [0,0]
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    #try:
    scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
    #print('present_url',scraping_url)  
    #print(tracking_num)
    options = Options()
    #options.add_argument('--headless=new')
    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    #driver.get('https://service.post.ch/ekp-web/ui/entry/search/' + str(tracking_num))
    driver.get(scraping_url)
    driver.implicitly_wait(20)
    """button = driver.find_element(By.CLASS_NAME,'more-btn')
    button.click()
    translate = driver.find_element(By.CLASS_NAME,'translate')
    translate =translate.find_element(By.TAG_NAME,'label')
    translate.click()
    sleep(5)"""
        
    Track_nums = []
    Codes = []
    Dates = []
    Times = []
    Descs = []
    Locs = []
    EventZipCode=[]
    IsInHouse = []
    
    list = []
    #list = driver.find_element(By.CLASS_NAME,'tracking-list-package-content')
    #list = list.find_elements(By.TAG_NAME,'ul')
    for l in list:
        Table = l.find_elements(By.TAG_NAME,'li')
        #print('len',len(Table))

        for t in Table:
            date_time = t.find_element(By.TAG_NAME,'time').text
            date, time , format = date_time.split(" ")
            new_time = change_time_format(time,format)
            new_date = change_date_format(date)
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

    driver.quit()
    #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))
    df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs,EventZipCode,IsInHouse)        
    logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
    country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
    scraped_tracking_nos.append(str(tracking_num))
    return df

    """except Exception as e:
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        country_logger.info('Error: '+ str(e))
        if "Unable to locate element" in str(e):
            discarded_tracking_nos.append(str(tracking_num))
        else:
            failed_tracking_nos.append(str(tracking_num))
        return tocsv.emtpy_frame()"""

#get_trackinginfo(tracking_num)
def scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    tracking_info = tracking_info[:1]
    batch_size = 1
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)
