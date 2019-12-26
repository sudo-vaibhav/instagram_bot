import time
import bs4
import requests
from selenium import webdriver

class insta_bot:
    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        username_field=self.driver.find_element_by_name("username")
        username_field.send_keys(self.username)
        password_field=self.driver.find_element_by_name("password")
        password_field.send_keys(self.password)
        time.sleep(2)
        login_button=self.driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]""")
        login_button.click()
        time.sleep(2)
    def get_followers(self):
        self.driver.get("https://www.instagram.com/"+self.username)
        time.sleep(3)
        self.driver.find_element_by_partial_link_text("following").click()
        self.driver.execute_script("alert('Scroll to the bottom of followers list and when you are done scrolling to the bottom respond with y in the terminal where this bot is running:')")
        resp="n"
        while resp not in ["y","Y"]:
            resp=input("Are you done taking scrolling to the bottom of the following list?(y/n): ")
        following_data=[i.text for i in self.driver.find_elements_by_xpath("/html/body/div[4]/div/div[2]/ul/div/li")]
        profiles=[]
        for f in following_data:
            idx=f.index("\n")
            profiles.append(f[:idx])
        return profiles
    def like_recent(self):
        pass
        
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.driver=webdriver.Chrome("./chromedriver")
        self.login()
        self.followers=self.get_followers()

    


bot=insta_bot("username","password") 

