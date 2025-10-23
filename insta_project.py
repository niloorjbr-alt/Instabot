import os
import time
import pickle
from selenium import webdriver
import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

url = "https://www.instagram.com/"



class InstaBot:
    def __init__ (self , username , password , cookie_file , driver , ):
        self.driver = driver
        self.username = username
        self.password = password
        self.cookie_file = cookie_file

    def save_cookie(self ):
       
        self.driver.get(url)
        time.sleep(3)
        wait = WebDriverWait(self.driver, 100)

       # Accept cookies if present
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._a9--._ap36._asz1'))).click()
        except:
            pass
        # username
        wait.until(EC.element_to_be_clickable((By.XPATH , '//input[@name ="username"]'))).send_keys(self.username)
        time.sleep(3)
        # password
        wait.until(EC.element_to_be_clickable((By.XPATH , '//input[@type="password"]'))).send_keys(self.password)
        time.sleep(3)
        # login box
        wait.until(EC.element_to_be_clickable((By.XPATH , '//button[@type="submit"]'))).click()    
        time.sleep(60)
        try:
           # Insta icon
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg.x1lliihq.x1n2onr6.x5n08af')))
            # Save cookies after finding the Insta icon
            pickle.dump(self.driver.get_cookies(), open(self.cookie_file, "wb"))
            print(f"✅cookies saved . for {self.username}  ")
        except:
            print(f"Login failed for {self.username}. Cookie not saved. ❌")    
       

    def load_cookies(self):
        self.driver.get(url)
        cookies = pickle.load(open(self.cookie_file, "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                cookie.pop('expiry') 
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        print(f" Logged in with cookie : {self.username}  without CAPTCHA ✅")

    def login(self):
     
        if os.path.exists(self.cookie_file) and os.path.getsize(self.cookie_file) > 0:
            try:
                self.load_cookies()
            except:
                print(f"❌ cookie moshkel darad baraye :{self.username}  dasti vared kon .  ")
                self.save_cookie()
        else:
            self.save_cookie()
                
    def scroll_and_click(self, element):
        actions = ActionChains(driver)
        actions.move_to_element(element).pause(0.5).click().perform()


    def like_post(self, profile_url):
        self.driver.get(profile_url)
        wait = WebDriverWait(driver, 100)

        # Open the first post
        first_post = wait.until(EC.element_to_be_clickable((By.XPATH, '(//a[contains(@href, "/p/")])[1]')))
        first_post.click()
        # Wait for the post dialog to fully load.
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]')))
        time.sleep(2)

        i=1
       # The first ten posts
        while i <= 5:
            print(f"🔄 dar hale pardazesh poste {i}")

            try:
                # Focus on post dialog
                dialog = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]')))
                actions = ActionChains(driver)
                actions.move_to_element(dialog).click().perform()
                time.sleep(3)
                actions.send_keys('l').perform()
                print(f'post {i} like shod')
            except Exception as e:
                print(f"❌moshkel poste{i}: {e}")

           # Go to the next post with retry
            next_found = False
            for attempt in range(3):
                try:
                    next_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aaqg._aaqh')))
                    self.scroll_and_click(next_btn)
                    time.sleep(2)
                    next_found = True
                    break
                except:
                    driver.execute_script("window.scrollBy(100,0);")
                    time.sleep(2)

            if not next_found:
                print("پست بعدی پیدا نشد یا رسیدیم به آخر 🚫")
                break

            i += 1

        print(" Hame post ha like shodand . ✅")   
       # Return to profile page
        # self.driver.get(profile_url)

    def comment(self , profile_url , comments):
            self.driver.get(profile_url)
            wait = WebDriverWait(driver , 50)
            # باز کردن اولین پست
            first_post = wait.until(EC.element_to_be_clickable((By.XPATH, '(//a[contains(@href, "/p/")])[1]')))
            first_post.click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]')))
            time.sleep(2)
            i=1
            while i <= 5:
                print(f"🔄 dar hale pardazesh poste {i}")

                try:
                    dialog = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]')))
                    actions = ActionChains(driver)
                    actions.move_to_element(dialog).click().perform()
                    time.sleep(2)
                    comment_input = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Add a comment…"]')))
                    comment_input.click()
                    time.sleep(2)
                    pyautogui.typewrite(comments , interval= 0.05)
                    time.sleep(3)
                    pyautogui.press("enter")

                    print(f'post {i} comment shod . ✅')
                        
                except :
                    print(f" post{i} commnet nashod .❌")

               
                next_found = False
                for attempt in range(3):
                    try:
                        next_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aaqg._aaqh')))
                        self.scroll_and_click(next_btn)
                        time.sleep(2)
                        next_found = True
                        break
                    except:
                        driver.execute_script("window.scrollBy(100,0);")
                        time.sleep(2)

                if not next_found:
                    print("پست بعدی پیدا نشد یا رسیدیم به آخر 🚫")
                    break

                i += 1

            print(" Hame post ha like shodand . ✅")   
            # driver.get(profile_url)
        
    def follow(self , profile_url):
        self.driver.get(profile_url)
        wait = WebDriverWait(driver , 50)

        follow_acount = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button//div[contains(text(),"Follow")]'))
        )
        follow_acount.click()


# # # -------- Run multiple accounts--------

users=[
        {
        "username" : "",
        "password" : "" , 
        "cookie" : "insta1.pkl"
    },
    # {
    #     "username" : "",
    #     "password" : "",
    #     "cookie" : "insta2.pkl"
    # }

]
for u in users:
    # برای هر اکانت یک مرورگر جدا تعریف شود
    chrome_options = Options()    # باز ماندن درایور
    chrome_options.add_experimental_option("detach", True)  # ✅ مرورگر باز می‌مونه
    service = Service("chromedriver.exe")  # مسیر chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    bot  = InstaBot(users["username"] , users["password"] , users['cookie'] , driver)
    bot.login() 
    # bot.like_post('https://www.instagram.com/nikkarimi/')
    # bot.comment('https://www.instagram.com/nikkarimi/' , "wow")
    bot.follow('https://www.instagram.com/nikkarimi/')
    # اجرای یوزر بعدی با زدن دکمه اینتر 
    input(f"accunt {users['username']} kamel shod baraye badi enter kon.")
    driver.quit()  # بسته شدن درایور
