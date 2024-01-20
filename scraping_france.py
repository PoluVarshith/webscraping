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
The site itself has a button to change french into english
"""
def get_trackinginfo(trackng_num):
    options = Options()
    #options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://www.laposte.fr/outils/track-a-parcel')
    #driver.maximize_window()
    driver.implicitly_wait(100)
    track = driver.find_element(By.NAME,'code')
    track.send_keys('LV770224450US')
    track.send_keys(Keys.RETURN)
    driver.implicitly_wait(20)

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
                elif j.get_attribute('class') == "showResults__label green":
                    EventDesc.append(j.get_attribute("innerText"))

    #drver.quit()
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for i in EventDate:
        #dt = i.split('·')
        track_num.append(trackng_num)
        Dates.append(i)
        Times.append('-')
        Loc.append('-')
    print(len(Dates),len(Times),len(EventDesc))

    
    Data = {
    'Tracking Number' : track_num,
    'EventDesc' : EventDesc,
    'EventDate' : Dates,
    'EventTime' : Times,
    'EventLocation' : Loc
    }
    df = pd.DataFrame(Data)
    print(df[['EventDesc','EventDate','EventTime','EventLocation']])

tracking_num ='LV770224450US'
get_trackinginfo(tracking_num)
