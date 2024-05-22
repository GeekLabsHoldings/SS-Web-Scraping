from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pytz
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

    
def PostDetail(driver, AttachedPosts):
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//div[@class="text-neutral-content"]')))
        text = driver.find_element(By.XPATH, '//div[@class="text-neutral-content"]').text
        for i in range(len(TickerList)):
            pattern = fr'\b{re.escape(TickerList[i])}\b'
            if re.search(pattern, text):
                TickerCount[i] = TickerCount[i] + 1
        AttachedPosts = AttachedPosts + 1
    except TimeoutException:
        pass

def PostComments(driver):
    comments = driver.find_elements(By.XPATH, '//*[@id="comment-tree"]/shreddit-comment/div[@slot="comment"]')
    for i in range(len(comments)):
        CommentText = comments[i].text
        for i in range(len(TickerList)):
            pattern = fr'\b{re.escape(TickerList[i])}\b'
            if re.search(pattern, CommentText):
                TickerCommentCount[i] = TickerCommentCount[i] + 1
        

input_list = input("Enter the Stock lists separate by spaces ")
TickerList = input_list.split()
TickerCount = [0]*len(TickerList)
TickerCommentCount = [0]*len(TickerList)
driver = webdriver.Chrome()
driver.maximize_window()



driver.get(f"https://www.reddit.com/r/wallstreetbets/comments/1cx5ldi/sonos_shades_of_electric_objects_sono/")
sleep(5)
AttachedPosts = 0
PostDetail(driver, AttachedPosts)
PostComments(driver)
                   
for i in range(len(TickerList)):
    print(f"The ticker '{TickerList[i]}' appears {TickerCount[i]} time(s) in posts and appears {TickerCommentCount[i]} time(s) in the the comments.")

##################################################################
close = input("press any key to close the window")
driver.quit()