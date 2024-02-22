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
"""
This website can track more than one shipment
"""
COUNTRY = 'GERMANY'
def change_date_format(date):
    #print(date)
    new_date = date
    #print(new_date)
    return new_date

def get_trackinginfo(tracking_num,scraping_tracking_nos,scraping_url,country_logger,log_country_dir_path=None):
    #tracking_num ='CY139955908US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        #url = ('https://www.deutschepost.de/int-verfolgen/data/search?piececode=' + str(tracking_num) + '&inputSearch=true&language=en')
        """options = Options()
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )"""
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(scraping_url)
        #print(driver.page_source)
        data = driver.find_element(By.TAG_NAME,'body').text
        data = json.loads(data)
        #print(type(data))
        try :
            events = data['sendungen'][0]['sendungsdetails']['sendungsverlauf']['events']
        except:
            #print("too many shipments with one tracking number?")
            return tocsv.emtpy_frame()
        #print(len(events))
        driver.close()
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        for i in events:
            if 'status' in i.keys() and i['status'] not in  ["",'null'] :
                Track_nums.append(tracking_num)
                Codes.append('')
                Descs.append(i['status'])
                date,time = i['datum'].split('T')
                #print(date,time)
                new_date = change_date_format(date)
                Dates.append(new_date)
                Times.append(time)
                try:
                    Locs.append(i['ort'])
                except:
                    Locs.append('')
        #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))
        df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs)
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraping_tracking_nos.append(str(tracking_num))
        return df
    except Exception as e:
        print(e)
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        #country_logger.info('Scraping_Url : '+ str(scraping_url))
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)
    
def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit):
    #print(len(tracking_nums))
    tracking_nums = tracking_nums[:5]
    batch_size = 5
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit)

