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
COUNTRY = 'AUSTRIA'
def get_trackinginfo(tracking_num,scraping_tracking_nos,scraping_url,country_logger,log_country_dir_path):
    #tracking_num = 'CY140541041US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        options = Options()
        options.add_argument('--headless=new')
        print(tracking_num)
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        driver.get(scraping_url)
        #driver.get('https://www.post.at/s/sendungsdetails?snr=CJ499904901US')
        #driver.maximize_window()
        driver.implicitly_wait(10)
        #track = driver.find_element(By.NAME,'tracking_search')
        #rack.send_keys(tracking_num)
        #track.send_keys(Keys.RETURN)
        #driver.implicitly_wait(20)

        Container = driver.find_element(By.CLASS_NAME,'tracking__history-list')
        CourseEntries = Container.find_elements(By.XPATH,'./*')

        Track_nums = []
        Descs = []
        Codes = []
        Dates = []
        Times = []
        Locs = []
        for i in CourseEntries:
            children = i.find_element(By.CLASS_NAME,'tracking__history-date')
            date = (children.get_attribute('innerText')).replace('\n',' ')
            details = i.find_element(By.CLASS_NAME,'tracking__history-details')
            time = details.find_element(By.CLASS_NAME,'tracking__history-time').get_attribute('innerText')
            #print(date,time)
            desc = details.find_element(By.CLASS_NAME,'tracking__history-status').get_attribute('innerText')
            desc = GoogleTranslator(source='auto', target='en').translate(desc)
            #print((desc))
            try:
                loc = details.find_element(By.CLASS_NAME,'tracking__history-location').get_attribute('innerText')
                #loc = GoogleTranslator(source='auto' , target='en').translate(loc)
            except Exception as e:
                #print(e)
                loc = '-'
            #print(loc)
            Track_nums.append(tracking_num)
            Codes.append('')
            Descs.append(desc)
            Dates.append(date)
            Times.append(time)
            Locs.append(loc)
        #print(len(Dates),len(Times),len(Descs))

        driver.quit()
        
        df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs)
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraping_tracking_nos.append(str(tracking_num))
        return df
    except Exception as e:
        #print(e)
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        return tocsv.emtpy_frame()

#tracking_num ='CJ499904901US'
#get_trackinginfo(tracking_num)

def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit):
    #print(len(tracking_nums))
    tracking_nums = tracking_nums[:5]
    batch_size = 5
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit)