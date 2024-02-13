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
                    elif j.get_attribute('class') in ["showResults__label green", "showResults__label blue"]:
                        EventDesc.append(j.get_attribute("innerText"))

        driver.quit()
        track_num = []
        Dates = []
        Times = []
        Loc = []
        for i in EventDate:
            #dt = i.split('·')
            track_num.append(tracking_num)
            Dates.append(i)
            Times.append('-')
            Loc.append('-')
        #print(len(Dates),len(Times),len(EventDesc))

        Data = {
        'Tracking Number' : track_num,
        'EventDesc' : EventDesc,
        'EventDate' : Dates,
        'EventTime' : Times,
        'EventLocation' : Loc
        }
        df = pd.DataFrame(Data)
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraping_tracking_nos.append(str(tracking_num))
        return df
    except:
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        return tocsv.emtpy_frame()
    
#get_trackinginfo(tracking_num)
def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit):
    #print(len(tracking_nums))
    tracking_nums = tracking_nums[:5]
    batch_size = 5
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit)
