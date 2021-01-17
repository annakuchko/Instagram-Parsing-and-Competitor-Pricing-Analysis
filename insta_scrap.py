#!/usr/bin/env python
# coding: utf-8


import time
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd


start = "\033[1m"
end = "\033[0;0m"

supported_versions_path = [
    'C:\\Users\\Asus\\Desktop\\chromedriver.exe'
]
username = str(input('Enter your username: '))
password = str(input('Enter your password: '))
hastag = '#'+str(input('Enter hashtag to search (without #): '))
instagram_link = "https://www.instagram.com/accounts/login/?source=auth_switcher"

opp = Options()
opp.add_argument('--blink-settings=imagesEnabled=false')
#opp.add_argument('--disable-gpu')

driver = webdriver.Chrome(
    executable_path = 'C:\\Users\\Asus\\Desktop\\chromedriver.exe', 
    options=opp
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
#move cursore to the search bar and insert hashtag
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((
        By.XPATH, 
        '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'
    ))
).send_keys(hastag)
#search for publications
WebDriverWait(driver, 20).until(
     EC.element_to_be_clickable((
         By.XPATH, 
         '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]'
     ))
).click()

comments = []
img_srcs = []
img_descs = []
likes = []
user_ids = []
#select the first publication
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((
        By.CLASS_NAME, 'eLAPa'
    ))
).click()

for i in range(10000):
    print(start+str(i)+end)
    try:
        #locate and save user id
        user_id = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "body > div._2dDPU.CkGkG > div.zZYga > div > article >"
                " header > div.o-MQd > div.PQo_0 > div.e1e1d > span > a"
            ))
        ).get_attribute('href')
        #locate and save link to the img
        img_src = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, '//img'
            ))
        ).get_attribute('src')
        #locate and save img description (instagram-generated)
        img_desc = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'div > div > div.KL4Bh'
            ))
        ).get_attribute('innerHTML').split('"')[1]
        
        try:
            #locate and save all available comments to the publication
            user_comments = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk'
            ))
            ).find_elements_by_class_name("C4VMK")
            
            #save each comment separately
            for c in user_comments:
                try:
                    comment = c.text
                    comments.append(comment)
                    user_ids.append(user_id)
                    img_srcs.append(img_src)
                    img_descs.append(img_desc)
                    try:
                        #locate and save likes if available
                        like = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((
                                By.CSS_SELECTOR,
                                'body > div._2dDPU.CkGkG > div.zZYga > div >'
                                ' article > div.eo2As > section.EDfFK.ygqzn > div > div > button'
                            ))
                        ).text
                        likes.append(like)
                    except:
                        print("No likes")
                        likes.append('NaN')
                except:
                    print("No comments")
                    comments.append('NaN')
                    user_ids.append(user_id)
                    img_srcs.append(img_src)
                    img_descs.append(img_desc)
                    try:
                        like = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((
                                By.CSS_SELECTOR,
                                'body > div._2dDPU.CkGkG > div.zZYga > div >'
                                ' article > div.eo2As > section.EDfFK.ygqzn > div > div > button'
                            ))
                        ).text
                        likes.append(like)
                    except:
                        print("No likes")
                        likes.append('NaN')

        except:
            comments.append('NaN')
            user_ids.append(user_id)
            img_srcs.append(img_src)
            img_descs.append(img_desc)
            
            try:
                like = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((
                                By.CSS_SELECTOR,
                                'body > div._2dDPU.CkGkG > div.zZYga > div >'
                                ' article > div.eo2As > section.EDfFK.ygqzn > div > div > button'
                            ))
                ).text
                likes.append(like)
            except:
                print("No likes")
                likes.append('NaN')
        
    except:
        print('Timeout')
    
    
    print('# of comments saved: ',len(comments))
    print('# of images saved: ',len(img_srcs))
    print('# of likes saved: ',len(likes))
    print('# of users saved: ',len(user_ids))
    print('# of descriptions saved: ',len(img_descs))
    
    #wait in case of bad Internet connection and switch to the next publication
    WebDriverWait(driver, 2000).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "body > div._2dDPU.CkGkG > div.EfHg9 > div >"
                " div > a._65Bje.coreSpriteRightPaginationArrow"
            ))
        ).click()


df = pd.DataFrame({
    'user_id':user_ids, 
    'img_src':img_srcs, 
    'comments':comments, 
    'likes':likes,
    'desc': img_descs
})

df.to_csv('insta_comments.csv')

