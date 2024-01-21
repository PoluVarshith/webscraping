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
This website can track more than one shipment
It needs 30 sec to load fully,  So implicitly_wait for 30
"""
def get_trackinginfo(trackng_num):
    options = Options()
    #options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://www.deutschepost.de/de/s/sendungsverfolgung.html?form.sendungsnummer=A0031FFBE60007DDE487')
    driver.implicitly_wait(100)
    track = driver.find_element(By.NAME,'piececode')
    track.send_keys(trackng_num)
    track.send_keys(Keys.RETURN)
    driver.implicitly_wait(20)

    CourseEntries = driver.find_elements(By.CLASS_NAME,'courseText')
    EventDate = []
    EventDesc = []
    for i in CourseEntries:
        children = i.find_elements(By.XPATH,'.//*')
        for j in children:
            if j.get_attribute("class") == "courseHeader":
                EventDate.append(j.get_attribute("innerText"))
            elif j.get_attribute('class') == "status":
                desc = j.get_attribute("innerText")
                desc = GoogleTranslator(source='auto', target='en').translate(desc)
                EventDesc.append(desc)

    driver.quit()
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
    for i in tracking_nums[:4]:
        dfs.append(get_trackinginfo(i[0]))

    country_frame = tocsv.country_csv()
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv('GERMANY')