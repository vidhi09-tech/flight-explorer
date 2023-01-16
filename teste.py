import pandas as pd

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())

from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\Users\rafae\OneDrive\Documentos\.wdm\drivers\geckodriver\win64\v0.32.0\geckodriver.exe', options=options)
driver.get('http://google.com/')

import time
url = "https://www.kayak.com/flights"
driver.get(url)
time.sleep(1)
from selenium.common.exceptions import NoSuchElementException

# Close cookies pop-up
accept_cookies_xpath = '/html/body/div[12]/div/div[3]/div/div/div/div/div[1]/div/div[2]/div[2]/div[1]/button/span'
accept_cookies_xpath =  '/html/body/div/div[1]/div/div[1]/div[2]/svg/path[1]'
try:
   driver.find_element_by_xpath(accept_cookies_xpath).click()
except NoSuchElementException:
   pass
 
 
departure = 'OPO' # Paris
arrival = 'LIS' # Tunis
departure_date = '2023-01-15' # Under the format 'YYYY-MM-DD'
arrival_date = '2023-01-15'
flexibility_option = "flexible" #for +/-3 days

url = f"https://www.kayak.com/flights/{departure}-{arrival}/{departure_date}-{flexibility_option}/{arrival_date}-{flexibility_option}"
driver.get(url)
xpath = '//tag_name[contains(@id, ‘static_text’)]'
xpath = '//*[contains(@id, "destinaton-airport-display-inner")]'
from selenium.webdriver.common.keys import Keys
# From
from_click_xpath = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/input'
from_text_xpath = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/input'


departure = 'Porto'
driver.find_element_by_xpath(from_click_xpath).click()
driver.find_element_by_xpath(from_text_xpath).send_keys(Keys.BACKSPACE + Keys.BACKSPACE + departure)
time.sleep(0.5)
driver.find_element_by_xpath(from_text_xpath).send_keys(Keys.RETURN)
time.sleep(1)


to_click_xpath = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/div'
to_text_xpath = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/input'

arrival = 'Lisbon'
driver.find_element_by_xpath(from_click_xpath).click()
driver.find_element_by_xpath(from_text_xpath).send_keys(Keys.BACKSPACE + Keys.BACKSPACE + arrival)
time.sleep(0.5)
driver.find_element_by_xpath(from_text_xpath).send_keys(Keys.RETURN)
time.sleep(1)


#https://medium.com/analytics-vidhya/what-if-selenium-could-do-a-better-job-than-your-travel-agency-5e4e74de08b0
#https://towardsdatascience.com/how-to-analyze-survey-data-with-python-84eff9cc9568
#https://www.youtube.com/watch?v=nN0OD6HLDJk
#https://github.com/kcelebi/Flight_Analysis
#https://github.com/g-ziyan/STAT_545A_547M_Exploratory_Data_Analysis/blob/2054c6da07023e132713e34152921f8a408bac67/class%20exercise/cm112/cm112.Rmd
