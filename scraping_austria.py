from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import goslate
"""
This website can track more than one shipment
It needs 30 sec to load fully,  So wai implicitly_wait for 30
"""

options = Options()
#options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options,
    # other properties...
)
driver.get('https://www.post.at/s/sendungssuche')
#driver.maximize_window()
driver.implicitly_wait(50)
track = driver.find_element(By.NAME,'tracking_search')
track.send_keys('CJ499904901US')
track.send_keys(Keys.RETURN)
driver.implicitly_wait(20)

element = driver.find_element(By.CLASS_NAME,'tracking__history')
text = (element.get_attribute("innerText"))
print(text)
gs = goslate.Goslate()
translated_text = gs.translate(text, 'en')
print(translated_text)
#driver.quit()
