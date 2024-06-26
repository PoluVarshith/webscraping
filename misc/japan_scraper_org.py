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
import logfuns
import snowflake_queries
import scraper
"""
The site itself has a button to change french into english
"""
COUNTRY = 'JAPAN'
def change_date_format(date):
    #print(date)
    m,d,y = date.split('/')
    new_date = '/'.join([y,m,d])
    #print(new_date)
    return new_date

def get_trackinginfo(tracking_num,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data):
    #options = Options()
    #options.add_argument('--headless=new')
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        """driver = webdriver.Chrome(
            options=options,
            # other properties...
        )"""
        driver = webdriver.Edge()
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        #driver.get('https://trackings.post.japanpost.jp/services/srv/search/direct?reqCodeNo1=' + str(tracking_num) + '&searchKind=S002&locale=en') 
        driver.get(scraping_url)
        #driver.maximize_window()
        driver.implicitly_wait(50)

        Table = driver.find_elements(By.CLASS_NAME,'tableType01.txt_c.m_b5')[1]
        #print((Table))
        #table = Table.find_elements(By.XPATH,'./*')[1]
        body = Table.find_elements(By.XPATH,'./*')[0]
        CourseEntries = body.find_elements(By.XPATH,'./*')
    except Exception as e:
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        country_logger.info('Error: '+ str(e))
        if "list index out of range" in str(e):
            discarded_tracking_nos.append(str(tracking_num))
        else:
            failed_tracking_nos.append(str(tracking_num))
        return tocsv.emtpy_frame()
    
    #print(len(CourseEntries))
    Track_nums = []
    Codes = []
    Dates = []
    Times = []
    Descs = []
    Locs = []
    EventZipCode = []
    IsInHouse = []
    for i in range(2,len(CourseEntries),2):
        date_time = CourseEntries[i].find_element(By.CLASS_NAME,'w_120').get_attribute('innerText')
        try:
            date,time = date_time.split(" ")
            date = change_date_format(date)
        except Exception as e:
        #print(e)
            date = date_time
            time = " "
        #print(date,time)
        desc = CourseEntries[i].find_element(By.CLASS_NAME,'w_150').get_attribute('innerText')
        #print(desc)
        locs = CourseEntries[i].find_elements(By.CLASS_NAME,'w_105')
        loc0 = locs[0].get_attribute('innerText')
        loc2 = locs[1].get_attribute('innerText')
        loc1 = CourseEntries[i+1].find_element(By.CLASS_NAME,'w_105').get_attribute('innerText')
        loc = loc0 +  ' ' + loc1 +' '+ loc2
        #print(loc)
        Track_nums.append(tracking_num)
        Codes.append('')
        Descs.append(desc)
        Dates.append(date)
        Times.append(time)
        Locs.append(loc)
        EventZipCode.append('')
        IsInHouse.append("FALSE")

    #print('lengths',len(Dates),len(Times),len(Descs),len(Times),len(Track_nums))
    driver.quit()
    df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs,EventZipCode,IsInHouse)
    logger.info(str(df[['EventDesc','EventDate','EventTime','EventLocation']]))
    country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
    scraped_tracking_nos.append(str(tracking_num))
    return df


#get_trackinginfo(tracking_num)

def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    #print(len(tracking_nums))
    #tracking_nums= tracking_nums[:1]
    batch_size = 5  #20 
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)
