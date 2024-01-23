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
"""
The site itself has a button to change french into english
"""
COUNTRY = 'JAPAN'
def get_trackinginfo(tracking_num):
    options = Options()
    options.add_argument('--headless=new')
    print(tracking_num)
    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://trackings.post.japanpost.jp/services/srv/search/direct?reqCodeNo1=' + str(tracking_num) + '&searchKind=S002&locale=en')
    #driver.maximize_window()
    driver.implicitly_wait(50)

    Table = driver.find_elements(By.CLASS_NAME,'tableType01.txt_c.m_b5')[1]
    #print((Table))
    #table = Table.find_elements(By.XPATH,'./*')[1]
    body = Table.find_elements(By.XPATH,'./*')[0]
    CourseEntries = body.find_elements(By.XPATH,'./*')
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
    print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    return df


#tracking_num ='CY139490872US'
#get_trackinginfo(tracking_num)
def scrape_list(tracking_nums):
    #print(len(tracking_nums))
    dfs = []
    threads =[]
    for i in tracking_nums[:4]:
        threads.append(twrv.ThreadWithReturnValue(target=get_trackinginfo, args=(i[0],)))
    
    for t in threads:
        t.start()

    for t in threads:
        dfs.append(t.join())

    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv()
