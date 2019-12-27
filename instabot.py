import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("user-data-dir=/Users/vaibhavchopra/Library/Application Support/Google/Chrome/Default")



class insta_bot:
    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3.5)
        username_field=self.driver.find_element_by_name("username")
        username_field.send_keys(self.username)
        password_field=self.driver.find_element_by_name("password")
        password_field.send_keys(self.password)
        time.sleep(3.5)
        login_button=self.driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]""")
        login_button.click()
        time.sleep(3.5)
    def count_calc(self,pstring):
        temp=list(pstring.split()[0])
        while "," in temp:
            temp.remove(",")
        return int("".join(temp))

    def like_recent_of_given(self,profile):
        self.driver.get("https://www.instagram.com/"+profile)
        time.sleep(3)
        posts_count_string=self.driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[1]""").text
        posts_count=self.count_calc(posts_count_string)
        if posts_count>0:
            most_recent_post=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div/div/div/div/a')
            most_recent_post.click()
            time.sleep(3)
            like_button=self.driver.find_element_by_xpath('/html/body/div/div/div/article/div/section/span')
            if like_button.find_element_by_tag_name("span").get_attribute("aria-label")=="Like":
                like_button.click()
        else:
            print("no posts were there to like for {}".format(profile))

    def like_recent_of_following(self):
        following=self.read_following_from_file()
        for profile in following:
            self.like_recent_of_given(profile)

    def get_following(self):
        self.driver.get("https://www.instagram.com/"+self.username)
        time.sleep(3)
        following_elem=self.driver.find_element_by_partial_link_text("following")
        self.following_count=self.count_calc(following_elem.text.split()[0])
        self.driver.find_element_by_partial_link_text("following").click()
        time.sleep(3)
        return self.get_profiles()

    def get_followers(self):
        self.driver.get("https://www.instagram.com/"+self.username)
        time.sleep(3)
        followers_elem=self.driver.find_element_by_partial_link_text("followers")
        self.followers_count=self.count_calc(followers_elem.text.split()[0])-1
        self.driver.find_element_by_partial_link_text("followers").click()
        time.sleep(3)
        return self.get_profiles()

    def get_profiles(self):
        try:
            while True:
                time.sleep(3.5)
                x=self.driver.find_element_by_class_name("oMwYe")
                x.location_once_scrolled_into_view
        except:
            pass
        following_data=[i.text for i in self.driver.find_elements_by_xpath("/html/body/div[4]/div/div[2]/ul/div/li")]
        profiles=[]
        for f in following_data:
            idx=f.index("\n")
            profiles.append(f[:idx])
        return profiles
    def save_following_to_file(self):
        f=open("following","wb")
        profiles=self.get_following()
        pickle.dump(profiles,f)
        f.close()
    def save_followers_to_file(self):
        f=open("followers","wb")
        profiles=self.get_followers()
        pickle.dump(profiles,f)
        f.close()
    def read_following_from_file(self):
        f=open("following","rb")
        return(pickle.load(f))
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.driver = webdriver.Chrome(options=options)
        self.base_link="https://www.instagram.com/"
    def follow(self,profile):
        self.driver.get(self.base_link+profile)
        time.sleep(3.5)
        buttons=self.driver.find_elements_by_tag_name("button")
        for button in buttons:
            if button.text=="Follow":
                button.click()
                time.sleep(2)
                break

bot=insta_bot("_choprautomated_","Password@123")
