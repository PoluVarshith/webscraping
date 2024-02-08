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
COUNTRY = 'AUSTRIA'
def get_trackinginfo(tracking_num,scraping_url):
    options = Options()
    #options.add_argument('--headless=new')
    print(tracking_num)
    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    url = scraping_url.replace("#TRACKING_NUM#",str(tracking_num))
    driver.get(url)
    #driver.get('https://www.post.at/s/sendungsdetails?snr=CJ499904901US')
    #driver.maximize_window()
    driver.implicitly_wait(50)
    #track = driver.find_element(By.NAME,'tracking_search')
    #rack.send_keys(tracking_num)
    #track.send_keys(Keys.RETURN)
    #driver.implicitly_wait(20)

    Container = driver.find_element(By.CLASS_NAME,'tracking__history-list')
    CourseEntries = Container.find_elements(By.XPATH,'./*')
    EventDate = []
    EventDesc = []
    track_num = []
    Dates = []
    Times = []
    Loc = []
    for i in CourseEntries:
        children = i.find_element(By.CLASS_NAME,'tracking__history-date')
        date = (children.get_attribute('innerText')).replace('\n',' ')
        details = i.find_element(By.CLASS_NAME,'tracking__history-details')
        time = details.find_element(By.CLASS_NAME,'tracking__history-time').get_attribute('innerText')
        #print(date,time)
        desc = details.find_element(By.CLASS_NAME,'tracking__history-status').get_attribute('innerText')
        desc = GoogleTranslator(source='auto', target='en').translate(desc)
        #print((desc))
        try:
            loc = details.find_element(By.CLASS_NAME,'tracking__history-location').get_attribute('innerText')
            #loc = GoogleTranslator(source='auto' , target='en').translate(loc)
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
    print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    return df

#tracking_num ='CJ499904901US'
#get_trackinginfo(tracking_num)
def scrape_list(tracking_nums,scraping_url,output_path):
    #print(len(tracking_nums))
    dfs = []
    threads =[]
    for i in tracking_nums[:4]:
        threads.append(twrv.ThreadWithReturnValue(target=get_trackinginfo, args=(i[0],scraping_url,)))
    
    for t in threads:
        t.start()

    for t in threads:
        dfs.append(t.join())

    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv(output_path)
