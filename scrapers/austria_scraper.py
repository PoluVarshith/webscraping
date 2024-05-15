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
from time import sleep
from threading import Thread
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies
"""
This website can track more than one shipment
It needs 30 sec to load fully,  So wai implicitly_wait for 30
"""
COUNTRY = 'AUSTRIA'
def change_date_format(date):
    #print(date)
    month_dict = {'JÄN':'01','FEB':'02','MÄR':'03','ÄPR':'04','APR':'04','MAI':'05','JUN':'06','JUL':'07','ÄUG':'08','AUG':'08','SEP':'09','OKT':'10','NOV':'11','DEC':'12'}
    d,m = date.split(" ")
    d = "%02d" % int(d) if int(d) < 10 else d 
    m = month_dict[m]
    y = '2024'
    new_date = '/'.join([y,m,d])
    #print(new_date)
    return new_date

def get_trackinginfo(tracking_info,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data):
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    tracking_num,facility_code = tracking_info
    #tracking_num = 'CY141258667US'
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
        print('error ',e)

    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        """options = Options()
        options.add_argument('--headless=new')
        #print(tracking_num)
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )"""
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)
        chrome_options = webdriver.ChromeOptions()
        proxies_extension = proxies(username, password, endpoint, port)

        chrome_options.add_extension(proxies_extension)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get(scraping_url)
        #driver.get('https://www.post.at/s/sendungsdetails?snr=CJ499904901US')
        #driver.maximize_window()
        driver.implicitly_wait(20)
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
        EventZipCode = []
        IsInHouse = []
        for i in CourseEntries:
            children = i.find_element(By.CLASS_NAME,'tracking__history-date')
            date = (children.get_attribute('innerText')).replace('\n',' ')
            date = change_date_format(date)
            details = i.find_element(By.CLASS_NAME,'tracking__history-details')
            time = details.find_element(By.CLASS_NAME,'tracking__history-time').get_attribute('innerText')
            new_time,new_date = logfuns.change_time(time,date,offset)
            desc = details.find_element(By.CLASS_NAME,'tracking__history-status').get_attribute('innerText')
            desc = GoogleTranslator(source='auto', target='en').translate(desc)
            #print((desc))
            try:
                loc = details.find_element(By.CLASS_NAME,'tracking__history-location').get_attribute('innerText')
                #loc = GoogleTranslator(source='auto' , target='en').translate(loc)
                #print('location',tracking_num,loc)
            except Exception as e:
                #print(e)
                loc = ''
            if 'us' in loc.lower():
                #print("breaking")
                break
            #print(loc)
            Track_nums.append(tracking_num)
            Codes.append('')
            Descs.append(desc)
            Dates.append(new_date)
            Times.append(new_time)
            Locs.append(loc)
            EventZipCode.append('')
            IsInHouse.append("FALSE")
        #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))

        driver.quit()
        
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
        return tocsv.emtpy_frame()

#tracking_num ='CJ499904901US'
#get_trackinginfo(tracking_num)

def scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    #print(len(tracking_nums))
    #tracking_info = tracking_info[:1]
    batch_size = 3
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)