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
"""
The site itself has a button to change french into english
"""
COUNTRY = 'JAPAN'
def get_trackinginfo(tracking_num,scraping_url,country_logger,log_country_dir_path=None):
    options = Options()
    options.add_argument('--headless=new')
    country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num)
    logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        driver = webdriver.Chrome(
            options=options,
            # other properties...
        )
        #print(scraping_url)
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        #driver.get('https://trackings.post.japanpost.jp/services/srv/search/direct?reqCodeNo1=' + str(tracking_num) + '&searchKind=S002&locale=en')
        print(scraping_url)
        driver.get(scraping_url)
        #driver.maximize_window()
        driver.implicitly_wait(50)

        Table = driver.find_elements(By.CLASS_NAME,'tableType01.txt_c.m_b5')[1]
        #print((Table))
        #table = Table.find_elements(By.XPATH,'./*')[1]
        body = Table.find_elements(By.XPATH,'./*')[0]
        CourseEntries = body.find_elements(By.XPATH,'./*')
    except:
        country_logger.info(str(tracking_num)+ " scraping failed")
        return tocsv.emtpy_frame()
    
    #print(len(CourseEntries))
    EventDate = []
    EventDesc = []
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for i in range(2,len(CourseEntries),2):
        date_time = CourseEntries[i].find_element(By.CLASS_NAME,'w_120').get_attribute('innerText')
        try:
            date,time = date_time.split(" ")
        except:
            date = date_time
            time = " "
        #print(date,time)
        desc = CourseEntries[i].find_element(By.CLASS_NAME,'w_150').get_attribute('innerText')
        #print(desc)
        locs = CourseEntries[i].find_elements(By.CLASS_NAME,'w_105')
        loc0 = locs[0].get_attribute('innerText')
        loc2 = locs[1].get_attribute('innerText')
        loc1 = CourseEntries[i+1].find_element(By.CLASS_NAME,'w_105').get_attribute('innerText')
        loc = loc0 +  ' ' + loc1 +' '+ loc2
        #print(loc)
        track_num.append(tracking_num)
        EventDesc.append(desc)
        Dates.append(date)
        Times.append(time)
        Loc.append(loc)

    #print(len(Dates),len(Times),len(EventDesc))
    driver.quit()
    Data = {
    'Tracking Number' : track_num,
    'EventDesc' : EventDesc,
    'EventDate' : Dates,
    'EventTime' : Times,
    'EventLocation' : Loc
    }
    df = pd.DataFrame(Data)
    logger.info(str(df[['EventDesc','EventDate','EventTime','EventLocation']]))
    country_logger.info(str(tracking_num) +' scraping successful')
    return df


#get_trackinginfo(tracking_num)
def scrape_list(tracking_nums,scraping_url,output_path,logger,log_dir_path):
    #print(len(tracking_nums))
    log_country_dir_path = logfuns.make_logging_country_dir(COUNTRY,log_dir_path)
    country_logger = logfuns.set_logger(log_dir_path,country=COUNTRY)
    country_logger.info("Total Tracking Numbers :" + str(len(tracking_nums)))
    country_logger.info('List of Tracking Numbers ' + str(tracking_nums))
    dfs = []
    threads =[]
    for i in tracking_nums[:3]:
        threads.append(twrv.ThreadWithReturnValue(target=get_trackinginfo, args=(i[0],scraping_url,country_logger,log_country_dir_path,)))
    
    for t in threads:
        t.start()

    for t in threads:
        dfs.append(t.join())

    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv(output_path)
