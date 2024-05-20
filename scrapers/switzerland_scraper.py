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
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies
from time import sleep

COUNTRY = 'SWITZERLAND'
US_location_Entities = ['chicago','kennedy','miami','jamaica','los angeles','south hackensack','usmiaa','uslaxa']
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

def get_trackinginfo(tracking_info,scraped_tracking_nos,discarded_tracking_nos,failed_tracking_nos,scraping_url,country_logger,log_country_dir_path,config_data):
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    tracking_num,facility_code = tracking_info
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #tracking_num = 'CY141288363US '
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
        driver.quit()
        country_logger.info('End of Scraping for : '+ str(tracking_num))
        logger.info('proxy error:  '+str(e))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
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
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(scraping_url)
        #driver.implicitly_wait(10)
        
        main = driver.find_element(By.TAG_NAME,'ekp-event-timeline')
        try:
            main.find_element(By.CLASS_NAME,'text-link.me-3').send_keys(Keys.RETURN)
        except Exception as e:
            print("check if there is only one tab for the tracking number")
            #print("error :",e)
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
                new_time,new_date = logfuns.change_time(time,new_date,offset)
                dd = e.find_element(By.CLASS_NAME,'col-8.col-md-8.ps-3.d-flex').text
                dd_split = dd.split('\n')
                if len(dd_split) < 2:
                    desc = dd_split[0]
                    loc = ''
                else:
                    #print(dd)
                    desc = dd_split[0]
                    loc = dd_split[1]
                
                ignore = False
                ignore = bool([r for r in US_location_Entities if(r in loc.lower())])
                if ignore:
                   continue 
                else:
                    #print(loc,'loc',ignore)
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
        country_logger.info('End of Scraping for : '+ str(tracking_num))
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
        driver.quit()
        country_logger.info('End of Scraping for : '+ str(tracking_num))
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)
def scrape(tracking_info,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data):
    #tracking_info = tracking_info[:3]
    batch_size = 1
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_info,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit,output_dir_path,cur_run_id,config_data)
