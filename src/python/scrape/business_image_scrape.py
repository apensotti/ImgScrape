from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from extension import proxies
import requests
import io
from PIL import Image
import time
import csv
from tqdm import tqdm
import random

class ListingScrape:
    image_file_index = 345

    def __init__(self, google_search=""):
        self.google_search = google_search
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=self.chrome_options)        
        self.listings_dict = {}
        self.image_urls = []
        self.proxy_list = []
        

    def get_proxies(self):
        with open("C:\\Users\\alexp\\src\\ImgScrape\\proxy.csv", "r") as f:
            reader = csv.reader(f,delimiter=":")
            for row in reader:
                self.proxy_list.append({"user":row[0],"pass":row[1],"ip":row[2],"port":row[3]})

    def set_proxies(self,proxy_index):
        user = self.proxy_list[proxy_index]["user"]
        password = self.proxy_list[proxy_index]["pass"]
        ip_address = self.proxy_list[proxy_index]["ip"]
        port = self.proxy_list[proxy_index]["port"]

        proxies_extension = proxies(user,password,ip_address,port)
        self.chrome_options.add_extension(proxies_extension)  
        self.chrome_options.add_experimental_option('detach',True)
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=self.chrome_options)

    def test_proxies(self):
        iptest_url = "https://myexternalip.com/raw"

        ip_address = self.proxy_list[0]['ip']
        self.driver.get(iptest_url) 
        ip_true = self.driver.find_element(By.CSS_SELECTOR, "pre").get_attribute("innerHTML")

        if ip_address == ip_true:
            print("Proxy Connected")
        else:
            print("Proxy Failed to Connect")

    def initiate_driver(self):
        options = self.chrome_options
        options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)


    def search_google_maps(self):
        img_url = "https://www.google.com/search?q=drywall+chicago&sca_esv=583219155&rlz=1C1CHBF_enUS830US830&biw=1920&bih=931&tbm=lcl&ei=M-9YZZHGJYav0PEPubya2AQ&oq=drywall+chicago&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIg9kcnl3YWxsIGNoaWNhZ28qAggAMgUQABiABDIGEAAYFhgeMgYQABgWGB4yCBAAGBYYHhgPMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeSKo_UPcGWNUvcAJ4AJABAJgBf6AB0wmqAQM1Lje4AQHIAQD4AQHCAgsQABiABBiKBRiGA8ICCxAAGIAEGIoFGJECwgIHEAAYgAQYDcICChAAGIAEGIoFGEPCAg4QABiABBiKBRixAxiRAsICDhAAGIAEGIoFGMkDGJECwgILEAAYgAQYigUYkgPCAggQABiABBiSA8ICCBAAGIAEGLEDiAYB&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[41.9984806,-87.58136809999999],[41.7517225,-87.74741390000001]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
        self.driver.get(img_url) 
        search_box = self.driver.find_element(By.NAME,"q")
        search_box.clear()
        search_box.send_keys(self.google_search)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

    def listings(self):
        listings = self.driver.find_elements(By.CLASS_NAME,"dbg0pd")
        self.listings_dict[self.google_search] = listings
        return self.listings_dict[self.google_search]
    
    def open_listing(self,listing_index):
        close_click = self.driver.execute_script("return document.getElementsByClassName('dbg0pd').item({0})".format(listing_index))
        try:
            self.driver.execute_script("arguments[0].click();", close_click)
            time.sleep(2)
        except:
            print("|__Failed: Listing Click")

    def open_images(self):
        image_click = self.driver.find_elements(By.CLASS_NAME,"yOf5Ze")
        try:
            image_click[0].click()
            time.sleep(3)
        except:
            print("|__Failed: Open Images Failed")
            pass

    def close_image_preview(self):
        close_click = self.driver.execute_script("return document.getElementsByClassName('tN4Gf syzQLe A1UKib s3DPGe Rj2Mlf OLiIxf PDpWxe LQeN7 kOhBoc s73B3c VtTx9b Q8G3mf').item(2)")
        try:
            self.driver.execute_script("arguments[0].click();",close_click)
        except:
            print('|__Failed: Close Image Preview')
            pass
    
    def close_images(self):
        close_click = self.driver.execute_script("return document.getElementsByClassName('CeiTH yHy1rc eT1oJ mN1ivc lDYWtd')[0]")
        try:
            self.driver.execute_script("arguments[0].click();",close_click)
        except:
            print('|__Failed: Close Images')
            pass

    def collect_image_urls(self):       
        images = self.driver.execute_script("return document.getElementsByClassName('m7eMIc XPukcf')")
        get_link_cmd = "return document.getElementsByClassName('m7eMIc XPukcf').item({0}).currentSrc"
        get_link_cmd2 = "return document.getElementsByClassName('m7eMIc XPukcf').item({0}).dataset['src']"
        try:
            for i in range(len(images)):
                if 'http' in self.driver.execute_script(get_link_cmd.format(i)):
                    self.image_urls.append(self.driver.execute_script(get_link_cmd.format(i)))
                elif 'http' in self.driver.execute_script(get_link_cmd2.format(i)):
                    self.image_urls.append(self.driver.execute_script(get_link_cmd2.format(i)))
                else:
                    pass
        except:
            pass
    
    def download_image(self,download_path,url,file_name):
        
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        with open (file_path, "wb") as f:
            image.save(f,"JPEG")
    
  
def main():
    scrape = ListingScrape(google_search='drywall repair chicago')
    scrape.get_proxies()
    scrape.set_proxies(0)
    time.sleep(2)
    scrape.search_google_maps()
    listings = scrape.listings()

    temp_list = []
    for i,l in enumerate(listings):
        print("listing {0}/{1}".format(i+1,len(listings)))
        if l not in temp_list:
            scrape.open_listing(i)
            time.sleep(2)
            scrape.open_images()
            time.sleep(2)
            scrape.close_image_preview()
            time.sleep(2)
            scrape.collect_image_urls()
            time.sleep(2)
            scrape.close_images()
            time.sleep(2)
            temp_list.append(l)

    temp_index = 0

    print("Downloading {0} images".format(scrape.image_urls))

    for url in scrape.image_urls:
            filename = "picture{0}.jpg".format(temp_index)
            scrape.download_image("C:\\Users\\alexp\\src\\ImgScrape\\img\\", url, filename)
            temp_index+=1

    print("Done")

def test_proxy_servers():
    obj = ListingScrape(google_search="")
    obj.get_proxies()
    obj.set_proxies(0)
    obj.test_proxies()

if __name__ == "__main__":
    main()





