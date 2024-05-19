from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pytz
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

input_string = input("Enter the Accounts: ")
RedditAccounts = input_string.split()

input_list = input("Enter the Stock lists separate by spaces ")
StockList = input_list.split()

time_frame = int(input("Enter the time interval in minutes for the scraping session: "))

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(f"https://www.reddit.com/" + RedditAccounts[0] + "/new/")
sleep(5)


posts = driver.find_elements(By.XPATH, "//article[@class='w-full m-0']")
for i, post in enumerate(posts):
    try:
        article = post.find_element(By.XPATH, ".//shreddit-post/a")
        href = article.get_attribute("href")
        
        driver.get(href)
        sleep(5)
        driver.back()
    
        posts = driver.find_elements(By.XPATH, "//article[@class='w-full m-0']")
    except StaleElementReferenceException:     
        posts = driver.find_elements(By.XPATH, "//article[@class='w-full m-0']")
        post = posts[i]  
        article = post.find_element(By.XPATH, ".//shreddit-post/a")
        href = article.get_attribute("href")        
        driver.get(href)
        sleep(5)
        driver.back()    

##################################################################
FlairClass = driver.find_element(By.XPATH, ".//shreddit-post-flair")
if "Meme" in FlairClass.text:
    print("Meme")
##################################################################
driver.execute_script(f"window.scrollBy(0, {1080});")
sleep(2)

##################################################################
close = input("press any key to close the window ")
driver.quit()

def TimeZone(time):
    timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    timestamp_utc = timestamp.replace(tzinfo=pytz.utc)
    
    cairo_timezone = pytz.timezone('Africa/Cairo')

    timestamp_cairo = timestamp_utc.astimezone(cairo_timezone)
   
    current_time_cairo = datetime.now(cairo_timezone)

    time_difference = current_time_cairo - timestamp_cairo

    minutes_difference = int(time_difference.total_seconds() / 60)
    return minutes_difference

# def CheckTimeInterval():
#     if time < time_frame:
#         return True
#     else:
#         return False


