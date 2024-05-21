from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pytz
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def TimeZone(time):
    timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    timestamp_utc = timestamp.replace(tzinfo=pytz.utc)
    
    cairo_timezone = pytz.timezone('Africa/Cairo')

    timestamp_cairo = timestamp_utc.astimezone(cairo_timezone)
   
    current_time_cairo = datetime.now(cairo_timezone)

    time_difference = current_time_cairo - timestamp_cairo

    day_difference = float(time_difference.total_seconds() / 86400)
    return day_difference

def ScrolllingTillTimeMeet():
    while True:
        posts = driver.find_elements(By.XPATH, "//article[@class='w-full m-0']")
        LatestPost = posts[len(posts)-1]
        TimePosted = LatestPost.find_element(By.XPATH, ".//time").get_attribute('datetime')
        TimeInDays = TimeZone(TimePosted)
        if TimeInDays < time_frame:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        else:
            break
        
    print(f"total Posts in the account = {len(posts)}")

def CheckTime(post):
    TimePosted = post.find_element(By.XPATH, ".//time").get_attribute('datetime')
    TimeInDays = TimeZone(TimePosted)
    if TimeInDays < time_frame:
        return True
    else:
        return False

def CheckFlair(post):
    FlairClass = post.find_element(By.XPATH, ".//shreddit-post-flair")
    if "Meme" in FlairClass.text or "MEME" in FlairClass.text or "meme" in FlairClass.text:
        return True
    else:
        return False
    
def PostDetail(driver, AttachedPosts):
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//div[@class="text-neutral-content"]')))
        text = driver.find_element(By.XPATH, '//div[@class="text-neutral-content"]').text
        for i in range(len(TickerList)):
            if TickerList[i] in text:
                TickerCount[i] = TickerCount[i] + 1  
        AttachedPosts = AttachedPosts + 1
    except TimeoutException:
        pass

def PostComments(driver):
    comments = driver.find_elements(By.XPATH, '//*[@id="comment-tree"]/shreddit-comment/div[@slot="comment"]')
    for i in range(len(comments)):
        CommentText = comments[i].text
        for i in range(len(TickerList)):
            if TickerList[i] in CommentText:
                TickerCommentCount[i] = TickerCommentCount[i] + 1
        

input_string = input("Enter the Accounts: ")
RedditAccounts = input_string.split()
input_list = input("Enter the Stock lists separate by spaces ")
TickerList = input_list.split()
TickerCount = [0]*len(TickerList)
TickerCommentCount = [0]*len(TickerList)
time_frame = int(input("Enter the time interval in minutes for the scraping session: "))
driver = webdriver.Chrome()
driver.maximize_window()


for account in RedditAccounts:
    driver.get(f"https://www.reddit.com/" + account + "/new/")
    sleep(5)

    ScrolllingTillTimeMeet()
    AttachedPosts = 0
    posts = driver.find_elements(By.XPATH, "//article[@class='w-full m-0']")
    original_window = driver.current_window_handle
    for post in posts:
        if CheckTime(post):
            if CheckFlair(post):
                continue
            else:
                article = post.find_element(By.XPATH, ".//shreddit-post/a")
                href = article.get_attribute("href")
                driver.execute_script("window.open(arguments[0]);", href)
                driver.switch_to.window(driver.window_handles[-1]) 
                PostDetail(driver, AttachedPosts)
                PostComments(driver)
                driver.close()
                driver.switch_to.window(original_window)
        else:
            break                       
for i in range(len(TickerList)):
    print(f"The ticker '{TickerList[i]}' appears {TickerCount[i]} time(s) in posts and appears {TickerCommentCount[i]} time(s) in the the comments.")

##################################################################
close = input("press any key to close the window")
driver.quit() 

