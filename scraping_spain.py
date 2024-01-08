from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
"""
Spain website can only track one item
It needs 30 sec to load fully,  So wai implicitly_wait for 30
It only give Delivary time and data no location
"""
def get_trackinginfo(trackng_num):
    options = Options()
    #options.add_argument('--headless=new')

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

    #element = driver.find_element(By.CLASS_NAME,'correos-ui-tracking-stepper__root.vertical.sc-correos-ui-tracking-stepper.sc-correos-ui-tracking-stepper-s')
    #print(element.get_attribute("innerText"))
    #print(element)
    date_times = driver.find_elements(By.CLASS_NAME,'correos-ui-tracking-stepper__date.sc-correos-ui-tracking-stepper')
    desc = driver.find_elements(By.CLASS_NAME,"correos-ui-tracking-stepper__desc.sc-correos-ui-tracking-stepper")
    EventDate = []
    EventDesc = []
    for i in desc[1::]:
        #print(i.get_attribute("innerText"))
        parent = i.find_element(By.XPATH,"./..");
        #print(parent.get_attribute("class"))
        if (parent.get_attribute("class") == "correos-ui-tracking-stepper__body correos-ui-tracking-stepper__body--border-bottom sc-correos-ui-tracking-stepper" ):
            children = parent.find_elements(By.XPATH,'.//*')
            for j in children:
                #print(j.get_attribute("innerText"))
                if j.get_attribute("class") == "correos-ui-tracking-stepper__date sc-correos-ui-tracking-stepper":
                    #print(j.get_attribute("innerText"))
                    EventDate.append(j.get_attribute("innerText"))
                elif j.get_attribute('class') == "correos-ui-tracking-stepper__desc sc-correos-ui-tracking-stepper":
                    #print(j.get_attribute('innerText'))
                    EventDesc.append(j.get_attribute("innerText"))

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
    print(len(Dates),len(Times),len(EventDesc))

    import pandas as pd
    Data = {
    'Tracking Number' : track_num,
    'EventDesc' : EventDesc,
    'EventDate' : Dates,
    'EventTime' : Times,
    'EventLocation' : Loc
    }
    df = pd.DataFrame(Data)
    print(df)

tracking_num ='CY139353845US'
get_trackinginfo(tracking_num)


"""
import requests
from bs4 import BeautifulSoup

URL = "https://www.correos.es/es/en/tools/tracker/items/details?tracking-number=CY139379406US"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "lxml")
obj = soup.find_all('div',class__= "correos-ui-tracking-stepper__date sc-correos-ui-tracking-stepper")
print(obj)"""
#correos-ui-tracking-stepper__date sc-correos-ui-tracking-stepper
#correos-ui-tracking-stepper__desc sc-correos-ui-tracking-stepper
#driver.quit()


#//*[@id="private-area-content"]/correos-cdk-section-box[1]/div/div/div/div[2]/div[1]/correos-cdk-shipping-card/div/div[3]/div/correos-ui-tracking-stepper/div/div/div[3]/div/div/div[1]/div/div/div[2]/span[1]
#//*[@id="private-area-content"]/correos-cdk-section-box[1]/div/div/div/div[2]/div[1]/correos-cdk-shipping-card/div/div[3]/div/correos-ui-tracking-stepper/div/div/div[3]/div/div/div[1]/div/div/div[2]/span[2]
#
