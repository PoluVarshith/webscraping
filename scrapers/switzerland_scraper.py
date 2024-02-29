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
"""
"""
COUNTRY = 'SWITZERLAND'
def change_date_format(date):
    #print(date)
    month_dict = {'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}
    day , dmy = date.split(',')
    dmy = dmy.strip()
    d,m,y = dmy.split(" ")
    m = m.lower()
    m = month_dict[m]
    new_date = '/'.join([y,m,d])
    #print(new_date)
    return new_date

def get_trackinginfo(tracking_num,scraping_tracking_nos,scraping_url,country_logger,log_country_dir_path):
    #tracking_num = 'CY140486433US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        #print(tracking_num)
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )
        #driver.get('https://service.post.ch/ekp-web/ui/entry/search/' + str(tracking_num))
        driver.get(scraping_url)
        driver.implicitly_wait(20)
        
        main = driver.find_element(By.TAG_NAME,'ekp-event-timeline')
        main.find_element(By.CLASS_NAME,'text-link.mr-3').send_keys(Keys.RETURN)
        Table = main.find_elements(By.CLASS_NAME,'pt-2')
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        EventZipCode=[]
        IsInHouse = []
        for t in Table:
            date = t.find_elements(By.CLASS_NAME,'sub-menu-item')[0].text
            events = t.find_elements(By.TAG_NAME,'ekp-event-item')
            new_date = change_date_format(date)
            for e in events:
                time = e.find_element(By.CLASS_NAME,'col-1.time').text
                Dates.append(new_date)
                Times.append(time)
                Track_nums.append(tracking_num)
                Codes.append('')
                #print('datetime',new_date,time)
                dd = e.find_element(By.CLASS_NAME,'pl-3').text
                desc,loc = dd.split('\n')
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
