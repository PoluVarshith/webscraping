from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from deep_translator import GoogleTranslator
import pandas as pd

from PIL import Image
from captcha_solver import CaptchaSolver
"""
This website can track more than one shipment
It needs 30 sec to load fully,  So wai implicitly_wait for 30
"""
COUNTRY = 'BRAZIL'
def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image


def get_trackinginfo(trackng_num):
    options = Options()
    #options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options,
        # other properties...
    )
    driver.get('https://www2.correios.com.br/sistemas/rastreamento/default.cfm')
    #driver.maximize_window()
    driver.implicitly_wait(50)
    track = driver.find_element(By.ID,'objeto')
    captcha_entry = driver.find_element(By.ID,'captcha')
    button = driver.find_element(By.ID,'b-pesquisar')
    track.send_keys(tracking_num)
    img = driver.find_element(By.ID,'captcha_image')
    get_captcha(driver, img, "captcha.png")
    #captcha solving function
    

    captcha_entry.send_keys()
    #track.send_keys(Keys.RETURN)
    button.click()
    driver.implicitly_wait(100)

    Table = driver.find_element(By.CLASS_NAME,'table.table-hover.spacer-xs-top-10.spacer-xs-bottom-0')
    table = Table.find_elements(By.XPATH,'./*')[1]
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


tracking_num ='CY139466887US'
get_trackinginfo(tracking_num)
