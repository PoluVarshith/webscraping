from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from deep_translator import GoogleTranslator
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
    #mb-3
    driver.get('https://postnl.post/details/?barcodes=UT141382960NL')
    #driver.maximize_window()
    driver.implicitly_wait(50)
    track = driver.find_element(By.ID,'barcodeId0')
    track.send_keys(tracking_num)
    track.send_keys(Keys.RETURN)
    blast = driver.find_element(By.CLASS_NAME,'btn.btn-primary.mx-auto.text-white')
    blast.click()
    driver.implicitly_wait(20)

    Table = driver.find_elements(By.CLASS_NAME,'table.table-sm.table-borderless.history')[0]
    table = Table.find_elements(By.XPATH,'./*')[1]
    #print(table)
    Container = table.find_elements(By.XPATH,'./*')
    print(len(Container))
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
        track_num.append(trackng_num)
        EventDesc.append(desc)
        Dates.append(date)
        Times.append(time)
        Loc.append(loc)
    print(len(Dates),len(Times),len(EventDesc))

    #drver.quit()
    import pandas as pd
    Data = {
    'Tracking Number' : track_num,
    'EventDesc' : EventDesc,
    'EventDate' : Dates,
    'EventTime' : Times,
    'EventLocation' : Loc
    }
    df = pd.DataFrame(Data)
    print(df[['EventDesc','EventDate','EventTime','EventLocation']])


tracking_num ='CK139527405NL'
get_trackinginfo(tracking_num)
