#!/usr/bin/env python
# coding: utf-8

subscribers = []

import time
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
start = "\033[1m"
end = "\033[0;0m"

supported_versions_path = [
    'C:\\Users\\Asus\\Desktop\\chromedriver.exe'
]
username = str(input('Enter your username: '))
password = str(input('Enter your password: '))

instagram_link = "https://www.instagram.com/accounts/login/?source=auth_switcher"

opp = Options()
opp.add_argument('--blink-settings=imagesEnabled=false')
#opp.add_argument('--disable-gpu')

driver = webdriver.Chrome(
    executable_path = 'C:\\Users\\Asus\\Desktop\\chromedriver.exe'
)            
#open instagram login screen, insert username
driver.get(instagram_link)
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR, "input[name='username']"
    ))
).send_keys(username)
#insert pass
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR, "input[name='password']"
    ))
).send_keys(password)
#login
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR, "input[name='password']"
    ))
).send_keys(Keys.RETURN)
time.sleep(2.5)
#retrieve all unique users profiles links
urls = df['user_id'].unique()

driver.get(urls[0])

#collect data on number of posts, subscribers and subscriptions for each profile
sub = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((
    By.CSS_SELECTOR,
    '#react-root > section > main > div > ul'
))
                                     ).text
print(sub)
subscribers.append(sub)

#open each profile in new tab
for url in urls[1:]:
    driver.get(url)
    sub = WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#react-root > section > main > div > ul'
))
                                     ).text
    print(sub)
    subscribers.append(sub)

df_profiles = pd.DataFrame({
    'user_id':urls, 
    'stats': subscribers
})
df_profiles.to_csv('df_profiles.csv')

