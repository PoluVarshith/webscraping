from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from deep_translator import GoogleTranslator
import pandas as pd

import requests
from bs4 import BeautifulSoup
"""
This website can track more than one shipment
It needs 30 sec to load fully,  So wai implicitly_wait for 30
"""
def get_trackinginfo(trackng_num):
    options = Options()
    #options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    URL = 'https://www.postnord.se/en/our-tools/track-and-trace?shipmentId=' + str(tracking_num)
    driver.get(URL)
    #driver.maximize_window()
    driver.implicitly_wait(50)

    Table = driver.find_element(By.CLASS_NAME,'')
    print(Table)
    table = Table.find_elements(By.XPATH,'./*')
    print(len(table))
    CourseEntries = table.find_elements(By.XPATH,'./*')
    print(len(CourseEntries))
    EventDate = []
    EventDesc = []
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for i in CourseEntries:
        date ,time = i.find_element(By.CLASS_NAME,'ng-binding').get_attribute('innerText').split(" ")
        #print(date,time)
        desc = i.find_element(By.CLASS_NAME,'text-xs-left.ng-binding').get_attribute('innerText')
        desc = GoogleTranslator(source='auto', target='en').translate(desc)
        #print((desc))
        try:
            j = i.find_elements(By.XPATH,'./*')[2]
            loc = (j.get_attribute('innerText')).split('\n')[3]
            loc = GoogleTranslator(source='auto' , target='en').translate(loc)
        except:
            loc = '-'
        #print(loc)
        track_num.append(trackng_num)
        EventDesc.append(desc)
        Dates.append(date)
        Times.append(time)
        Loc.append(loc)
    print(len(Dates),len(Times),len(EventDesc))

    #drver.quit()
    Data = {
    'Tracking Number' : track_num,
    'EventDesc' : EventDesc,
    'EventDate' : Dates,
    'EventTime' : Times,
    'EventLocation' : Loc
    }
    df = pd.DataFrame(Data)
    print(df[['EventDesc','EventDate','EventTime','EventLocation']])


tracking_num ='LX567513734US'
get_trackinginfo(tracking_num)
