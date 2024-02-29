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
The site itself has a button to change french into english
"""
COUNTRY = 'FRANCE'
def change_date_format(date):
    #print(date)
    month_dict = {'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}
    day ,d = date.split(",")
    d = d.strip()
    d,m = d.split(" ")
    m = m.lower()
    m = month_dict[m]
    y = '2024'
    new_date = '/'.join([y,m,d])
    #print(new_date)
    return new_date

def get_trackinginfo(tracking_num,scraping_tracking_nos,scraping_url,country_logger,log_country_dir_path):
    #tracking_num = 'CY140541041US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try :
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        driver.get(scraping_url)
        #driver.get('https://www.laposte.fr/outils/track-a-parcel')
        #driver.maximize_window()
        driver.implicitly_wait(20)
        #track = driver.find_element(By.NAME,'code')
        #track.send_keys(tracking_num)
        #track.send_keys(Keys.RETURN)
        #driver.implicitly_wait(20)

        date_times = driver.find_elements(By.CLASS_NAME,'showResults__date')
        EventDate = []
        EventDesc = []
        for i in date_times:
            parent = i.find_element(By.XPATH,"./..");
            if (parent.get_attribute("class") == "showResults__item" ):
                children = parent.find_elements(By.XPATH,'.//*')
                for j in children:
                    if j.get_attribute("class") == "showResults__date":
                        EventDate.append(j.get_attribute("innerText"))
                    elif j.get_attribute('class') in ["showResults__label green", "showResults__label blue",'showResults__label red']:
                        EventDesc.append(j.get_attribute("innerText"))

        driver.quit()
        #print((str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url)))
        Track_nums = []
        Codes = []
        Descs = EventDesc
        Dates = []
        Times = []
        Locs = []
        EventZipCode = []
        IsInHouse=[]
        for i in EventDate:
            #dt = i.split('·')
            Track_nums.append(tracking_num)
            Codes.append('')
            new_date = change_date_format(i)
            Dates.append(new_date)
            Times.append('')
            Locs.append('')
            EventZipCode.append('')
            IsInHouse.append("FALSE")
        #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))

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
def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit):
    #print(len(tracking_nums))
    tracking_nums = tracking_nums[:5]
    batch_size = 5
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit)
