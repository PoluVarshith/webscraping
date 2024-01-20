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
Spain website can only track one item
It needs 30 sec to load fully,  So wait implicitly_wait for 30
It only give Delivary time and data no location
"""
def get_standard_date_time(date_time):
    print('nothing done yet')


def get_trackinginfo(trackng_num):
    options = Options()
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://www.correos.es/es/en/tools/tracker/items')
    #driver.maximize_window()
    driver.implicitly_wait(100)
    track = driver.find_element(By.NAME,'tracking-number')
    track.send_keys(trackng_num)
    track.send_keys(Keys.RETURN)
    driver.implicitly_wait(20)

    date_times = driver.find_elements(By.CLASS_NAME,'correos-ui-tracking-stepper__date.sc-correos-ui-tracking-stepper')
    desc = driver.find_elements(By.CLASS_NAME,"correos-ui-tracking-stepper__desc.sc-correos-ui-tracking-stepper")
    EventDate = []
    EventDesc = []
    for i in desc[1::]:
        parent = i.find_element(By.XPATH,"./..");
        if (parent.get_attribute("class") == "correos-ui-tracking-stepper__body correos-ui-tracking-stepper__body--border-bottom sc-correos-ui-tracking-stepper" ):
            children = parent.find_elements(By.XPATH,'.//*')
            for j in children:
                if j.get_attribute("class") == "correos-ui-tracking-stepper__date sc-correos-ui-tracking-stepper":
                    EventDate.append(j.get_attribute("innerText"))
                elif j.get_attribute('class') == "correos-ui-tracking-stepper__desc sc-correos-ui-tracking-stepper":
                    EventDesc.append(j.get_attribute("innerText"))

    driver.quit()
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for i in EventDate:
        dt = i.split('·')
        track_num.append(trackng_num)
        Dates.append(dt[0])
        Times.append(dt[1])
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
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    return df

def scrape_list(tracking_nums):
    #print(len(tracking_nums))
    #tracking_num ='CY139353845US'
    #get_trackinginfo(tracking_num)
    dfs = []
    threads =[]
    for i in tracking_nums[:4]:
        threads.append(twrv.ThreadWithReturnValue(target=get_trackinginfo, args=(i[0],)))
    
    for t in threads:
        t.start()

    # Wait for all threads to finish.
    for t in threads:
        dfs.append(t.join())

    country_frame = tocsv.country_csv()
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv()
