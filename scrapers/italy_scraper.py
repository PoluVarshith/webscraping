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
It needs 30 sec to load fully,  So wai implicitly_wait for 30
"""
COUNTRY = 'ITALY'
def get_trackinginfo(tracking_num,scraping_url):
    options = Options()
    #options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
    driver.get(url)
    #driver.get('https://www.poste.it/cerca/index.html#/risultati-spedizioni/LV770247402US')
    #driver.maximize_window()
    driver.implicitly_wait(50)
    #track = driver.find_element(By.CLASS_NAME,'form-control')
    #track.send_keys(tracking_num)
    #track.send_keys(Keys.RETURN)
    #driver.implicitly_wait(30)

    Table = driver.find_element(By.CLASS_NAME,'table.table-hover.spacer-xs-top-10.spacer-xs-bottom-0')
    table = Table.find_elements(By.XPATH,'./*')[1]
    CourseEntries = table.find_elements(By.XPATH,'./*')
    #print(len(CourseEntries))
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
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    return df

#tracking_num ='LV770247402US'
#get_trackinginfo(tracking_num)

def scrape_list(tracking_nums,scraping_url,output_name):
    #print(len(tracking_nums))
    dfs = []
    for i in tracking_nums[:4]:
        dfs.append(get_trackinginfo(i[0],scraping_url))

    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv(output_path)