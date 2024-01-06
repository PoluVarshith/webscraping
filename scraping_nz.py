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

options = Options()
#options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options,
    # other properties...
)
driver.get('https://www.nzpost.co.nz/tools/tracking')
#driver.maximize_window()
driver.implicitly_wait(100)
track = driver.find_element(By.NAME,'TrackParcel')
track.send_keys('LV770506124US')
track.send_keys(Keys.RETURN)
driver.implicitly_wait(50)

element = driver.find_element(By.CLASS_NAME,'HistoryCard_content__2b_mw')
print(element.get_attribute("innerText"))

# release the resources allocated by Selenium and shut down the browser
#driver.quit()
