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
COUNTRY = 'FRANCE'
def get_trackinginfo(tracking_num):
    options = Options()
    #options.add_argument('--headless=new')
    print(tracking_num)
    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://www.laposte.fr/outils/track-a-parcel')
    #driver.maximize_window()
    driver.implicitly_wait(100)
    track = driver.find_element(By.NAME,'code')
    track.send_keys(tracking_num)
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

    driver.quit()
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for i in EventDate:
        #dt = i.split('·')
        track_num.append(tracking_num)
        Dates.append(i)
        Times.append('-')
        Loc.append('-')
    #print(len(Dates),len(Times),len(EventDesc))

    
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

#tracking_num ='LV770224450US'
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
