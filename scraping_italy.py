from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import goslate

"""
The site itself has a button to change french into english
"""

options = Options()
#options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options,
    # other properties...
)
driver.get('https://www.poste.it/')
#driver.maximize_window()
driver.implicitly_wait(30)
track = driver.find_element(By.CLASS_NAME,'form-control')
print(track)
track.send_keys('LV770247402US')
track.send_keys(Keys.RETURN)
driver.implicitly_wait(20)

element = driver.find_element(By.CLASS_NAME,'table-responsive.spacer-xs-top-10')
text = (element.get_attribute("innerText"))
print(text)
gs = goslate.Goslate()
translated_text = gs.translate(text, 'en')
print(translated_text)
#driver.quit()
