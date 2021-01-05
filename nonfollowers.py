#usr/bin/python3.8
from selenium import webdriver
from time import sleep
from datetime import date, datetime
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

username = '<YOUR USERNAME HERE>'
password = '<YOUR PASSWORD HERE>'

class InstaUnfollowers:
    def __init__(self, username, password):
        global response
        self.username = username
        self.password = password
        
        self.driver = webdriver.Chrome(ChromeDriverManager().install()) #webdriver.Firefox() to use Firefox
        self.driver.set_window_size(600, 1080)
        self.driver.set_window_position(1000, 0)
        self.driver.get("https://instagram.com")
        sleep(2)
        # instagram login
        print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] Logging In")
        username_type = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
        username_type.send_keys(username)
        password_type = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
        password_type.send_keys(password)
        submit = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
        submit.click()
        sleep(3)
        try:
            ad = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Successful LogIn")
            ad.click()
            sleep(3)
            ad = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
            ad.click()
        except:
            response = f"[{today.strftime('%Y-%m-%d')} {now.strftime('%H:%M:%S')}] Sorry, username or password was incorrect." + \
                       f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Time expired"
            self.driver.close()
    def get_unfollowers(self):
        try:
            usernames = self.driver.find_element_by_xpath("/html/body/div/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img")
            usernames.click()
        
            profile = self.driver.find_element_by_xpath("/html/body/div/section/nav/div[2]/div/div/div[3]/div/div[5]/div/div/div/a/div/div[2]/div/div/div/div")
            profile.click()
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Accessing your profile")
            sleep(3)
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Now we need to check who you follow and who follows you")
            Following = self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")
            Following.click()
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Checking your followings")
            following = self.get_people(self.driver)
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Great! Now, we need to check your followers")
            Followers = self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")
            Followers.click()
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Checking your followers")
            followers = self.get_people(self.driver)      
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Finally, comparing both (following and followers)")
            not_following_back = [user for user in following if user not in followers]
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Writing in a txt file...")
            with open('Unfollowers.txt', 'w') as file:
                for i in range(len(not_following_back)):
                    file.write(not_following_back[i])
                    file.write('\n')

            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Writing the DataFrame in terminal...")
            pd.set_option('display.max_rows', len(not_following_back))

            Unfollowers = pd.DataFrame(data=not_following_back, columns=['Unfollowers'])
            print(Unfollowers)

            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Writing in a xlsx file...")
            writer = pd.ExcelWriter('Unfollowers.xlsx')

            Unfollowers.to_excel(writer)
            # save the excel
            writer.save()
            print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] File saved")
        except:
            response = f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{self.username}] Time expired"

    def get_people(self, url):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

        prev_height, height = 0, 1
        while prev_height != height:
            prev_height = height
            sleep(1) # In case of any problem, change sleep parameter
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # url.get('https://instagram.com/'+username) # close follower/following window by accessing instagram.com/<username>
        close = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div[2]/button")
        close.click()
        return names

today = date.today()
now = datetime.now()
try:
    instabot = InstaUnfollowers(username, password)
    instabot.get_unfollowers()
    print(f"[{date.today().strftime('%Y-%m-%d')} {datetime.now().strftime('%H:%M:%S')}] [{username}] Closing window...")
    instabot.driver.close()
except:
    print(response)
