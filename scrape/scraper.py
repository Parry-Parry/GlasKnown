import os
from config import OBJECT_ID, PREFIX, EMAIL, PWORD
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from post import Post


class Scraper:
    def __init__(self):
        self.page_id = OBJECT_ID
        gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
        binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
        self.driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko + '.exe')
        self.posts = list()

    def scrape(self):
        main = "https://www.facebook.com/" + OBJECT_ID
        post_url = "https://facebook.com/hashtag/" + PREFIX.lower()
        self.driver.get(main)

        self.driver.find_element_by_xpath("//button[@title='Accept All']").click()

        username = self.driver.find_element_by_id("email")
        username.clear()
        username.send_keys(EMAIL)

        password = self.driver.find_element_by_name("pass")
        password.clear()
        password.send_keys(PWORD)

        self.driver.find_element_by_xpath("//input[@data-testid='royal_login_button']").click()
        self.driver.implicitly_wait(10)

        link = self.driver.find_elements_by_partial_link_text(PREFIX)[0]
        max_post = int(link.get_attribute('text').split('_')[-1])
        current = max_post

        for i in range(max_post):
            self.driver.get(post_url + str(current))
            self.driver.implicitly_wait(2)

            expand = self.driver.find_elements_by_partial_link_text('See more')
            if expand:
                expand[0].click()

            tmp_blocks = self.driver.find_elements_by_xpath("//div[@style='text-align: start;']")
            tmp = list()
            for b in tmp_blocks:
                text = b.text
                if text is not None:
                    tmp.append(text)

            self.posts.append(Post(tmp, current))
            current -= 1
