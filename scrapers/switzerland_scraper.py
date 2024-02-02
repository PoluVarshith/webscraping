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
"""
COUNTRY = 'SWITZERLAND'
def get_trackinginfo(tracking_num):
    tracking_num = 'CY140082734US'
    options = Options()
    #options.add_argument('--headless=new')
    print(tracking_num)
    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://service.post.ch/ekp-web/ui/entry/search/' + str(tracking_num))
    #driver.maximize_window()
    driver.implicitly_wait(100)

    Table = driver.find_elements(By.CLASS_NAME,'container-fluid.tab-content.ml-1')[0]
    date =  Table.find_elements(By.CLASS_NAME,'sub-menu-item')[0].text
    print('date',date)
    #print(len(Table))
    table = Table.find_elements(By.CLASS_NAME,'col-12')
    print('table',len(table))
    #print(len(Events))
    EventDate = []
    EventDesc = []
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for t in table:
        desc = t.find_element(By.CLASS_NAME,'col-1.time').get_attribute('innerText')
        print(desc)
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

#tracking_num = 'CY140082734US'
#get_trackinginfo(tracking_num)
def scrape_list(tracking_nums):
    #print(len(tracking_nums))
    dfs = []
    threads =[]
    for i in tracking_nums[:1]:
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
