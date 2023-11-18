from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import requests
import json
import io
from PIL import Image
import time

class ListingScrape:
    image_file_index = 0

    def __init__(self, google_search=""):
        self.google_search = google_search
        self.driver = None
        self.listings_dict = {}
        self.image_urls = []

    def initiate_driver(self):
        img_url = "https://www.google.com/search?q=drywall+chicago&sca_esv=583219155&rlz=1C1CHBF_enUS830US830&biw=1920&bih=931&tbm=lcl&ei=M-9YZZHGJYav0PEPubya2AQ&oq=drywall+chicago&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIg9kcnl3YWxsIGNoaWNhZ28qAggAMgUQABiABDIGEAAYFhgeMgYQABgWGB4yCBAAGBYYHhgPMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeSKo_UPcGWNUvcAJ4AJABAJgBf6AB0wmqAQM1Lje4AQHIAQD4AQHCAgsQABiABBiKBRiGA8ICCxAAGIAEGIoFGJECwgIHEAAYgAQYDcICChAAGIAEGIoFGEPCAg4QABiABBiKBRixAxiRAsICDhAAGIAEGIoFGMkDGJECwgILEAAYgAQYigUYkgPCAggQABiABBiSA8ICCBAAGIAEGLEDiAYB&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[41.9984806,-87.58136809999999],[41.7517225,-87.74741390000001]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
        options = Options()
        options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        self.driver.get(img_url) 

    def search_google_maps(self):
        # Find the search bar element and type your query
        search_box = self.driver.find_element(By.NAME,"q")
        search_box.clear()
        search_box.send_keys(self.google_search)

        # Press 'Enter' to perform the search
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        time.sleep(3)  # You can adjust the wait time based on your internet

    def listings(self):
        listings = self.driver.find_elements(By.CLASS_NAME,"dbg0pd")
        self.listings_dict[self.google_search] = listings
        return self.listings_dict[self.google_search]
    
    def open_listing(self,index):
        self.listings_dict[self.google_search][index].click()
        time.sleep(2)

    def open_images(self):
        image_click = self.driver.find_elements(By.CLASS_NAME,"yOf5Ze")
        try:
            image_click[0].click()
        except:
            pass
    
    def close_images(self):
        close_click = self.driver.execute_script("return document.getElementsByClassName('CeiTH yHy1rc eT1oJ mN1ivc lDYWtd')[0]")
        try:
            self.driver.execute_script("arguments[0].click();",close_click)
        except:
            pass

    def collect_image_urls(self):       

        images = self.driver.execute_script("return document.getElementsByClassName('m7eMIc aQg20b')")
        images

        get_link_cmd = "return document.getElementsByClassName('m7eMIc aQg20b').item({0}).currentSrc"
        get_link_cmd2 = "return document.getElementsByClassName('m7eMIc aQg20b').item({0}).dataset['src']"

        for i in range(len(images)):
            if 'http' in self.driver.execute_script(get_link_cmd.format(i)):
                self.image_urls.append(self.driver.execute_script(get_link_cmd.format(i)))
                print("link captured")
            elif 'http' in self.driver.execute_script(get_link_cmd2.format(i)):
                self.image_urls.append(self.driver.execute_script(get_link_cmd2.format(i)))
                print("link captured")
    
    def download_image(download_path,url,file_name):
        try:
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            file_path = download_path + file_name

            with open (file_path, "wb") as f:
                image.save(f,"JPEG")
            print("Success")
        except Exception as e:
            print('Failed -', e)

        print("Success")
    
    
        
        

scrape = ListingScrape(google_search='drywall repair boulder')
scrape.initiate_driver()
scrape.search_google_maps()
listings = scrape.listings()
#scrape.open_listing(0)
#scrape.open_images()
#scrape.collect_image_urls()

for i in range(8):
    scrape.open_listing(i)
    scrape.open_images()
    scrape.collect_image_urls()
    time.sleep(6)
    scrape.close_images()

temp_index = 0

#for i,url in enumerate(scrape.image_urls):
#        scrape.download_image("C:\\Users\\alexp\\src\\ImgScrape\\img\\", url=url, file_name="picture{0}.jpg".format(temp_index))
#        temp_index+=1

print(scrape.image_urls)





