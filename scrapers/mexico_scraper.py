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
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies
from time import sleep
from deep_translator import GoogleTranslator


COUNTRY = 'MEXICO'

def change_date_format(date):
    #print(date)
    dd,mm,yyyy = date.split("/")
    dd = "%02d" % int(dd)
    mm = "%02d" % int(mm)
    new_date = "/".join([yyyy,mm,dd])
    #print(new_date)
    return new_date

def change_time_format(time):
    #print(time)
    hr,mn,sec = time.split(":")
    dd = "%02d" % int(hr)
    mm = "%02d" % int(mn)
    new_time = ':'.join([hr,mn])
    #print(new_time)
    return new_time

def get_trackinginfo(tracking_info,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data):
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    tracking_num,facility_code = tracking_info
    #tracking_num = 'CY363884990US'
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
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #print('present_url',scraping_url)  
        #print(tracking_num)
        """options = Options()
        #options.add_argument('--headless=new')
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )"""
        #driver.get('https://service.post.ch/ekp-web/ui/entry/search/' + str(tracking_num))
        chrome_options = webdriver.ChromeOptions()
        proxies_extension = proxies(username, password, endpoint, port)

        chrome_options.add_extension(proxies_extension)
        #chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(scraping_url)
        driver.implicitly_wait(50)
        input = driver.find_element(By.CLASS_NAME,'col-sm-3.control-label')
        input.send_keys(tracking_num)
        button = driver.find_element(By.CLASS_NAME,'btn.btn-primary')
        button.click()
        #driver.implicitly_wait(100)
        #sleep(5)
            
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        EventZipCode=[]
        IsInHouse = []
        
        Table = driver.find_element(By.CLASS_NAME,'table.table-bordered')
        list = Table.find_elements(By.TAG_NAME,'tr')[1:]
        #print(len(list),'Total Events')
        for l in list:
            info = l.find_elements(By.TAG_NAME,'td')
            date = info[0].text
            time = info[1].text
            new_time = change_time_format(time)
            new_date = change_date_format(date)
            desc =info[3].text
            desc = GoogleTranslator(source='auto', target='en').translate(desc)
            desc = desc.replace('"','')
            loc = info[2].text
            loc = GoogleTranslator(source='auto', target='en').translate(loc)
            loc = loc.replace('"','')
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

    except Exception as e:
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        country_logger.info('Error: '+ str(e))
        if "Unable to locate element" in str(e):
            discarded_tracking_nos.append(str(tracking_num))
        else:
            failed_tracking_nos.append(str(tracking_num))
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)
def scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    #tracking_info = tracking_info[:1]
    batch_size = 3
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)
