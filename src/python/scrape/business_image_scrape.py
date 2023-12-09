from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from extension import proxies
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import io
from PIL import Image
import time
import csv
from tqdm import tqdm
import math

class ListingScrape:
    image_file_index = 6063

    def __init__(self,google_search=''):
        self.google_search = google_search
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=self.chrome_options)        
        self.listings_dict = {}
        self.image_elements = []
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
        self.driver.set_window_position(-1000,0)
        self.driver.maximize_window()
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

    def click_image(self, index):
        click_image = self.driver.execute_script("return document.getElementsByClassName('m7eMIc XPukcf')")
        exception = "return document.getElementsByClassName('m7eMIc XPukcf')[{0}].currentSrc"
        try:
            if "https://streetview" not in click_image[index].getAttribute('src'):
                self.driver.execute_script("arguments[0].click();",click_image[index])
            else:
                self.driver.execute_script("arguments[0].click();",click_image[index-2])
        except:
            pass

    def close_image_preview(self):
        close_click = self.driver.execute_script("return document.getElementsByClassName('tN4Gf syzQLe A1UKib s3DPGe Rj2Mlf OLiIxf PDpWxe LQeN7 kOhBoc s73B3c VtTx9b Q8G3mf').item(2)")
        try:
            self.driver.execute_script("arguments[0].click();",close_click)
        except:
            print('|__Failed: Close Image Preview')
            pass
    
    def load_images(self):
        try:
            last_height = self.driver.execute_script("return document.querySelector('.HHuGCe').scrollHeight")

            while True:            
                self.driver.execute_script("return document.querySelector('.HHuGCe').scrollTo(0,document.querySelector('.HHuGCe').scrollHeight)")

                time.sleep(1)

                new_height = self.driver.execute_script("return document.querySelector('.HHuGCe').scrollHeight")
                if new_height == last_height:
                    break 
                last_height = new_height
        except:
            pass
        
    def close_images(self):
        close_click = self.driver.execute_script("return document.getElementsByClassName('CeiTH yHy1rc eT1oJ mN1ivc lDYWtd')[0]")
        try:
            self.driver.execute_script("arguments[0].click();",close_click)
        except:
            print('|__Failed: Close Images')
            pass
    
    def carousel_click(self):
        try:
            button = self.driver.execute_script("return document.getElementsByClassName('m7eMIc XPukcf')")
            get_link_cmd = "return document.getElementsByClassName('m7eMIc aQg20b')"
            for i,link in enumerate(get_link_cmd):
                self.driver.execute_script("arguments[0].click()",button[3])
        except:
            pass

    def collect_image_urls2(self):
        #try:
            src = "return document.getElementsByClassName('m7eMIc aQg20b')[{0}].getAttribute('src')"
            data_src = "return document.getElementsByClassName('m7eMIc aQg20b')[{0}].getAttribute('data-src')"

            thumbnails = self.driver.execute_script("return document.getElementsByClassName('m7eMIc XPukcf')")
            thumbnail_link = "return document.getElementsByClassName('m7eMIc XPukcf')[{0}].getAttribute('src')"

            print(len(thumbnails))
            for i,link in enumerate(thumbnails):

                if i%5 == 0:
                    self.driver.execute_script("return document.querySelector('.HHuGCe').scrollBy(0,600)")

                try:
                    if 'streetview' not in self.driver.execute_script(thumbnail_link.format(i+5)):
                        self.driver.execute_script("arguments[0].click();",thumbnails[i+5])
                    else:
                        self.driver.execute_script("arguments[0].click();",thumbnails[i+6])
                except:
                    pass

                try:
                    if i%51 == 0:
                        images = self.driver.execute_script("return document.getElementsByClassName('m7eMIc aQg20b')")

                        for i,image in enumerate(images):
                            if 'data:image' in image.get_attribute('src'):
                                self.image_urls.append(image.get_attribute('data-src'))
                            else:
                                self.image_urls.append(image.get_attribute('src'))        
                except:
                    pass
    
    def download_image(self,download_path,url,file_name):
        try:
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            file_path = download_path + file_name
            with open (file_path, "wb") as f:
                image.save(f,"JPEG")
        except:
            pass

    def run_scrape(self,search):
        pass
        
    
def main():
    scrape = ListingScrape(google_search='drywall repair tampa fl')
    scrape.get_proxies()
    scrape.set_proxies(1)
    time.sleep(2)
    scrape.search_google_maps()
    listings = scrape.listings()

    temp_list = []
    for i,l in enumerate(listings):
        print("listing {0}/{1}".format(i+1,len(listings)))
        if l not in temp_list:
            scrape.open_listing(i)
            print('opening listing')
            time.sleep(1)
            print('opening images')
            scrape.open_images()
            time.sleep(1)
            print('loading images')
            scrape.load_images()
            time.sleep(1)
            print('collecting image links')         
            scrape.collect_image_urls2()
            time.sleep(1)
            print('next...')
            scrape.close_images()
            temp_list.append(l)

    print("Downloading {0} images".format(len(scrape.image_urls)))

    for i,url in enumerate(tqdm(scrape.image_urls,ncols=500)):
        filename = "picture{0}.jpg".format(ListingScrape.image_file_index)
        scrape.download_image("C:\\Users\\alexp\\src\\ImgScrape\\img\\", url, filename)
        ListingScrape.image_file_index+=1
            

    print("Done")

def test():
    obj = ListingScrape(google_search="drywall chicago")
    obj.get_proxies()
    obj.set_proxies(1)
    obj.search_google_maps()
    obj.open_listing(1)
    time.sleep(2)
    obj.open_images()
    time.sleep(2)
    obj.load_images()
    time.sleep(2)
    obj.collect_image_urls2()
    time.sleep(2)
    print("Downloading {0} images".format(len(obj.image_urls)))

    for i,url in enumerate(obj.image_urls):
        filename = "picture{0}.jpg".format(i)
        obj.download_image("C:\\Users\\alexp\\src\\ImgScrape\\img\\", url, filename)
        ListingScrape.image_file_index+=1
        time.sleep(1)
        
#
    print("Done")
    
if __name__ == "__main__":
    main()





