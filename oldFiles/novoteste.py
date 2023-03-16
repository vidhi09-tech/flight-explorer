from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import requests # 2
import json # 3
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 8)

from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)
    
driver = webdriver.Chrome(options = chrome_options)

depart = 'OPO'
destination = 'MAD'
#destinations = ['LIS', 'MAD']
#dates = ['2023-01-20', '2023-01-21']
date = '2023-01-20'

final_df = pd.DataFrame({'depart_from': [],
  'arrive_at': [],
  'date': [],
  'depart_time': [],
  'arrival_time': [],
  'price': [],
  'airline': [],
  'flight_duration': []})
  
#options = Options()
#options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
#driver = webdriver.Firefox(executable_path=r'C:\Users\rafae\OneDrive\Documentos\.wdm\drivers\geckodriver\win64\v0.32.0\geckodriver.exe', options=options)

url = f'https://www.kayak.com/flights/{depart}-{destination}/{date}?sort=price_a'
print(url)
#driver = webdriver.Firefox(executable_path=r'C:\Users\rafae\OneDrive\Documentos\.wdm\drivers\geckodriver\win64\v0.32.0\geckodriver.exe', options=options)
driver.implicitly_wait(20)
driver.get(url)
time.sleep(20)    
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# departure times
d_times_lst = []
d_times = soup.findAll('span', attrs={'class': 'depart-time base-time'})
for tm1 in d_times:
    d_times_lst.append(tm1.text)

# arrival times
a_times_lst = []
a_times = soup.findAll('span', attrs={'class': 'arrival-time base-time'})
for tm2 in a_times:
    a_times_lst.append(tm2.text)

# prices
price_lst = []
price_tag = re.compile('Common-Booking-MultiBookProvider(.*) Theme-featured-large(.*) multi-row(.*)')
prices = soup.findAll('div', attrs={'class': price_tag})
for price in prices:
    price_lst.append(price.text.split('\n')[4].strip())

# airlines
airline_lst = []
airlines = soup.findAll('div', attrs={'class': 'bottom', 'dir': 'ltr'})
for airline in airlines:
    airline_lst.append(airline.text.replace('\n', ''))
    
# durations
duration_lst = []
durations = soup.findAll('div', attrs={'class': 'section duration allow-multi-modal-icons'})
for duration in durations:
    duration_lst.append(' '.join(duration.text.split(' ')[:2]).replace('\n', ''))

df = pd.DataFrame({'depart_from': depart,
                   'arrive_at': destination,
                   'date': date,
                   'depart_time': d_times_lst[:15],
                   'arrival_time': a_times_lst[:15],
                   'price': price_lst[:15],
                   'airline': airline_lst[:15],
                   'flight_duration': duration_lst[:15]})
print(df)
final_df = pd.concat([final_df, df], ignore_index=True, sort=False)

driver.close()

time.sleep(20)

final_df.to_csv('kayak_flight_data.csv')
