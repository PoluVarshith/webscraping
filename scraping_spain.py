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
#divs = element.find_element(By.TAG_NAME,'')
x = element.find_element(By.CLASS_NAME,'correos-ui-tracking-stepper__body.sc-correos-ui-tracking-stepper')
print(x)
y = x.find_element(By.CLASS_NAME ,'correos-ui-tracking-stepper__date.sc-correos-ui-tracking-stepper')
print(y.get_attribute("innerText"))


a = element.find_element(By.CLASS_NAME,'lastItem.correos-ui-tracking-stepper__parentcontainer.correos-ui-tracking-stepper__parentcontainer--cursor.sc-correos-ui-tracking-stepper')
b = a.find_element(By.CLASS_NAME,'correos-ui-tracking-stepper__date.sc-correos-ui-tracking-stepper')
print(b.get_attribute('innerText'))
#info = element.find_element(By.CLASS_NAME,'correos-ui-tracking-stepper__container sc-correos-ui-tracking-stepper')
#for i in info:
#    print(i.text)
#shipping_card  = driver.find_element(By.CLASS_NAME,'cdk-shipping-card-detail sc-correos-cdk-shipping-card')
#print(shipping_card)
# release the resources allocated by Selenium and shut down the browser
#driver.quit()
