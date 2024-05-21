from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pytz
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()
action = ActionChains(driver)
driver.get(f"https://www.reddit.com/r/Shortsqueeze/comments/1cwq5m5/bullish_on_gwav_short_and_long_term/")
sleep(5)
i = int(0)

comments = driver.find_elements(By.XPATH, '//*[@id="comment-tree"]/shreddit-comment/div[@slot="comment"]')
input_list = input("Enter the Stock lists separate by spaces")
TickerList = input_list.split()
TickerCommentCount = [0]*len(TickerList)

for i in range(len(comments)):
    
    CommentText = comments[i].text
    print(CommentText)
    for i in range(len(TickerList)):
        if TickerList[i] in CommentText:
            TickerCommentCount[i] = TickerCommentCount[i] + 1
         
    
for i in range(len(TickerList)):
    print(f"The ticker '{TickerList[i]}' appears {TickerCommentCount[i]} time(s) in the text.")
 

