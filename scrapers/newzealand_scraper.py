from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from deep_translator import GoogleTranslator
import pandas as pd
"""
Spain website can only track one item
It needs 30 sec to load fully,  So wai implicitly_wait for 30
It only give Delivary time and data no location
"""
COUNTRY = 'NEW ZEALAND'
def get_trackinginfo(trackng_num):
    options = Options()
    #options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://www.nzpost.co.nz/tools/tracking?trackid=' + str(tracking_num))
    driver.implicitly_wait(50)

    Table = driver.find_element(By.CLASS_NAME,'HistoryCard_content__2b_mw')
    body = Table.find_elements(By.XPATH,'./*')[0]
    CourseEntries = body.find_elements(By.XPATH,'./*')
    print(len(CourseEntries))
    EventDate = []
    EventDesc = []
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for i in CourseEntries:
        desc = i.find_elements(By.XPATH,'./*')[0].get_attribute('innerText')
        entry = i.find_elements(By.XPATH,'./*')[1].get_attribute('innerText').split('\n')

        info = entry[0].split(',')
        time = info[0]
        date = info[1]
        loc = ' '.join(info[2::])
        print(desc,date,time,loc)

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

tracking_num ='LV770506124US'
get_trackinginfo(tracking_num)
