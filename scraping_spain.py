from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from bs4 import BeautifulSoup
"""
Spain website can only track one item
It needs 30 sec to load fully,  So wai implicitly_wait for 30
It only give Delivary time and data no location
"""

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
track.send_keys('CY139379406US')
track.send_keys(Keys.RETURN)
driver.implicitly_wait(20)

element = driver.find_element(By.CLASS_NAME,'correos-ui-tracking-stepper__root.vertical.sc-correos-ui-tracking-stepper.sc-correos-ui-tracking-stepper-s')
print(element.get_attribute("innerText"))
#print(element)
#driver.quit()
