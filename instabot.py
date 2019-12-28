import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime

options = Options()
options.add_argument("user-data-dir=<enter path here>")

class insta_bot:
    def follow_multiple_from_file(self,filename):
        profiles=self.read_profiles_from_file(filename)
        for profile in profiles:
            self.follow(profile)

    def login(self):
        password=input("enter password:")
        self.driver.get(self.base_link+"accounts/login/")
        time.sleep(3.5)
        username_field=self.driver.find_element_by_name("username")
        username_field.send_keys(self.username)
        password_field=self.driver.find_element_by_name("password")
        password_field.send_keys(password)
        time.sleep(3.5)
        login_button=self.driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]""")
        login_button.click()
        time.sleep(3.5)

    def count_calc(self,pstring):
        temp=list(pstring.split()[0])
        while "," in temp:
            temp.remove(",")
        return int("".join(temp))

    def like_recent_of_given(self,profile,following):
        self.driver.get(self.base_link+profile)
        time.sleep(3)
        current_posts_count=self.count_posts()
        if current_posts_count>following[profile]["last_posts_count"]:
            most_recent_post=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div/div/div/div/a')
            most_recent_post.click()
            time.sleep(3)
            like_button=self.driver.find_element_by_xpath('/html/body/div/div/div/article/div/section/span')
            if like_button.find_element_by_tag_name("span").get_attribute("aria-label")=="Like":   #this should always be true but still
                like_button.click()                    
        following[profile]["last_posts_count"]=current_posts_count
            
    def count_posts(self):
        current_posts_count_string=self.driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[1]""").text
        return self.count_calc(current_posts_count_string)
        

    def like_recent_of_following(self):
        following=self.read_profiles_from_file("following")
        for profile in following:
            last_time=datetime.datetime(day=following[profile]["last_checked"]["day"],month=following[profile]["last_checked"]["month"],year=following[profile]["last_checked"]["year"])
            current_time=datetime.datetime.now()
            if (current_time-last_time).total_seconds()>43200:
                self.like_recent_of_given(profile,following)
            following[profile]["last_checked"]["day"]=current_time.day
            following[profile]["last_checked"]["month"]=current_time.month
            following[profile]["last_checked"]["year"]=current_time.year
        self.update_db(following)

    def get_following(self):
        self.driver.get(self.base_link+self.username)
        time.sleep(3)
        following_elem=self.driver.find_element_by_partial_link_text("following")
        self.following_count=self.count_calc(following_elem.text.split()[0])
        self.driver.find_element_by_partial_link_text("following").click()
        time.sleep(3)
        return self.get_profiles_list()

    def get_followers(self):
        self.driver.get(self.base_link+self.username)
        time.sleep(3)
        followers_elem=self.driver.find_element_by_partial_link_text("followers")
        self.followers_count=self.count_calc(followers_elem.text.split()[0])-1
        self.driver.find_element_by_partial_link_text("followers").click()
        time.sleep(3)
        return self.get_profiles_list()

    def get_profiles_list(self):
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
    def update_db(self,profiles):
        f=open("following","wb")
        pickle.dump(profiles,f)

    def save_profiles_to_file(self,filename):
        f=open(filename,"wb")
        if filename=="following":
            profiles=self.profiles_dict_initialize(self.get_following())
        elif filename=="followers":
            profiles=self.profiles_dict_initialize(self.get_followers())
        pickle.dump(profiles,f)
        f.close()

    def profiles_dict_initialize(self,profiles):
        profiles_dict=dict()
        for username in profiles:
            profiles_dict[username]=dict()
            profiles_dict[username]["last_checked"]={"day":1,"month":1,"year":1}
            profiles_dict[username]["last_posts_count"]=0
        return profiles_dict
    def read_profiles_from_file(self,filename):
        if filename.endswith(".txt"):
            f=open(filename,'r')
            profiles=f.readlines()
            for profile in profiles:
                profile.strip("\n")
                profile.strip(" ")
            while "" in profiles:
                profiles.remove("")
            return self.profiles_dict_initialize(profiles)
        else:
            f=open(filename,"rb")
            return(pickle.load(f))
    def __init__(self,username):
        self.username=username
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
                profiles=self.read_profiles_from_file("following")
                current_time=datetime.datetime.now()
                profiles[profile]={"last_posts_count":self.count_posts(),"last_checked":{"day":current_time.day,"month":current_time.month,"year":current_time.year}}
                self.update_db(profiles)
                break

bot_name=input("Enter username of account to be automated:")
bot=insta_bot(bot_name)
login_needed=input("would you like to login? (y/n) :")
if login_needed=="y" or login_needed=="Y":
    bot.login()
update_needed=input("would you like to initialize following profiles' database: (y/n)")
if update_needed=="y" or update_needed=="Y":
    bot.save_profiles_to_file("following")
print("Now you can proceed with your commands")
