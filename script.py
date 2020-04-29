import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = webdriver.FirefoxOptions()
driver = webdriver.Chrome("/Users/tusharchopra/Desktop/Tushar/Work/Development/Websites/geckodriver", chrome_options=options)

import time

driver.get("https://roobet.com/crash")
driver.set_window_size(1920, 1200)
time.sleep(5)
driver.find_element_by_tag_name('body').send_keys(Keys.TAB)
driver.find_element_by_tag_name('body').send_keys(Keys.TAB)
driver.find_element_by_tag_name('body').send_keys(Keys.TAB)
driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
actions = ActionChains(driver)
#actions.move_by_offset( 795, 718).click().perform()
a = driver.find_element(By.CSS_SELECTOR, ".tick_2dJyV:nth-child(1)").text
df = pd.DataFrame([[a, pd.datetime.now()]], columns=(["Crash Point"], ["datetime"]))
df.to_csv("scraped.csv",  mode='a', header=False)
while True:
    b = driver.find_element(By.CSS_SELECTOR, ".tick_2dJyV:nth-child(1)").text
    if b != a:
        a = b
        bdf = pd.DataFrame([[b, pd.datetime.now()]], columns=(["Crash Point"], ["datetime"]))
        bdf.to_csv("scraped.csv", mode='a', header=False)
