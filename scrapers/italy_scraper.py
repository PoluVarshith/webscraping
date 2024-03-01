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
import scraper
import snowflake_queries
"""
This website can track more than one shipment
It needs 30 sec to load fully,  So wai implicitly_wait for 30
"""
COUNTRY = 'ITALY'
def change_date_format(date):
    #print(date)
    d,m,y = date.split('/')
    new_date = '/'.join([y,m,d])
    #print(new_date)
    return new_date
def change_time_format(time):
    new_time = time.replace('.',':')
    return new_time

def get_trackinginfo(tracking_num,scraping_tracking_nos,scraping_url,country_logger,log_country_dir_path):
    #tracking_num ='LV770378221US'
    tracking_num = 'CY140680851US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        driver.get(scraping_url)
        #driver.maximize_window()
        driver.implicitly_wait(20)
        #track = driver.find_element(By.CLASS_NAME,'form-control')
        #track.send_keys(tracking_num)
        #track.send_keys(Keys.RETURN)
        #driver.implicitly_wait(30)

        Table = driver.find_element(By.CLASS_NAME,'table.table-hover.spacer-xs-top-10.spacer-xs-bottom-0')
        table = Table.find_elements(By.XPATH,'./*')[1]
        CourseEntries = table.find_elements(By.XPATH,'./*')
        #print(len(CourseEntries))
        Track_nums = []
        Descs = []
        Codes = []
        Dates = []
        Times = []
        Locs = []
        EventZipCode = []
        IsInHouse = []
        for i in CourseEntries:
            date ,time = i.find_element(By.CLASS_NAME,'ng-binding').get_attribute('innerText').split(" ")
            #print(date,time)
            desc = i.find_element(By.CLASS_NAME,'text-xs-left.ng-binding').get_attribute('innerText')
            desc = GoogleTranslator(source='auto', target='en').translate(desc)
            #print((desc))
            try:
                j = i.find_elements(By.XPATH,'./*')[2]
                loc = (j.get_attribute('innerText')).split('\n')[3]
                loc = GoogleTranslator(source='auto' , target='en').translate(loc)
            except:
                loc = '-'
            #print(loc)
            Track_nums.append(tracking_num)
            Codes.append('')
            Descs.append(desc)
            new_date = change_date_format(date)
            Dates.append(new_date)
            new_time = change_time_format(time)
            Times.append(new_time)
            Locs.append(loc)
            EventZipCode.append('')
            IsInHouse.append("FALSE")
        #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))

        driver.quit()
        
        df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs,EventZipCode,IsInHouse)
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraping_tracking_nos.append(str(tracking_num))
        return df
    except Exception as e:
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        country_logger.info('Error: '+ str(e))
        return tocsv.emtpy_frame()


#get_trackinginfo(tracking_num)
def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path):
    #print(len(tracking_nums))
    tracking_nums = tracking_nums[:5]
    batch_size = 5
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path)
