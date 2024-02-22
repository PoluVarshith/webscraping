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
def get_trackinginfo(tracking_num,scraping_tracking_nos,scraping_url,country_logger,log_country_dir_path):
    tracking_num = 'CY140486433US'
    #country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    #logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        print('present_url',scraping_url)
        #print(tracking_num)
        options = Options()
        #options.add_argument('--headless=new')
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )
        #driver.get('https://service.post.ch/ekp-web/ui/entry/search/' + str(tracking_num))
        driver.get(scraping_url)
        #driver.maximize_window()
        driver.implicitly_wait(20)
        
        main = driver.find_element(By.TAG_NAME,'ekp-event-timeline')
        print(main)
        #python_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="detail"]/div[5]/ekp-tab-details/div/ekp-event-timeline/div/div[2]/div[1]/a')))
        #python_button.click() #click link
        #a = main.find_element(By.XPATH,'//*[@id="detail"]/div[5]/ekp-tab-details/div/ekp-event-timeline/div/div[2]/div[1]/a[@role = "button"]').click()
        main.find_element(By.CLASS_NAME,'text-link.mr-3').send_keys(Keys.RETURN)
        #print('aaaaa',a.get_attribute('innerText'))
        table = main.find_elements(By.CLASS_NAME,'pt-2')
        print('main',len(table))
        print('main',main.get_attribute('innerText'))
        Table = driver.find_elements(By.CLASS_NAME,'container-fluid.tab-content.ml-1')[0]
        date =  Table.find_elements(By.CLASS_NAME,'sub-menu-item')[0].text
        print('date',date)
        #print(len(Table))
        table = Table.find_elements(By.CLASS_NAME,'col-12')
        print('table',len(table))
        for t in table:
            print('here')
            print(t.get_attribute('innerText'))
        #print(len(Events))
        EventDate = []
        EventDesc = []
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        for t in table:
            desc = t.find_element(By.CLASS_NAME,'col-1 time').get_attribute('innerText')
            print(desc)
            locs = CourseEntries[i].find_elements(By.CLASS_NAME,'w_105')
            loc0 = locs[0].get_attribute('innerText')
            loc2 = locs[1].get_attribute('innerText')
            loc1 = CourseEntries[i+1].find_element(By.CLASS_NAME,'w_105').get_attribute('innerText')
            loc = loc0 +  ' ' + loc1 +' '+ loc2
            #print(loc)
            Track_nums.append(tracking_num)
            Descs.append(desc)
            Dates.append(date)
            Times.append(time)
            Locs.append(loc)

        #print(len(Dates),len(Times),len(EventDesc))
        driver.quit()
        #print(len(Track_nums),len(Codes),len(Descs),len(Dates),len(Times),len(Locs))
        df = tocsv.make_frame(Track_nums,Codes,Descs,Dates,Times,Locs)        
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful , Scraping_URL: ' + str(scraping_url))
        scraping_tracking_nos.append(str(tracking_num))
        return df

    except Exception as e:
        print(e)
        country_logger.info(str(tracking_num) +' scraping failed , Scraping_URL: ' + str(scraping_url))
        country_logger.info(e)
        return tocsv.emtpy_frame()

#tracking_num = 'CY140082734US'
#get_trackinginfo(tracking_num)
def scrape(tracking_nums,scraping_url,output_path,logger,log_dir_path,c_audit):
    #print(len(tracking_nums))
    tracking_nums = tracking_nums[:1]
    batch_size = 5
    scraper.scrape_list(COUNTRY,get_trackinginfo,tracking_nums,batch_size,scraping_url,output_path,logger,log_dir_path,c_audit)
