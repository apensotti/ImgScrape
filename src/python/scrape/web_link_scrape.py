from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import io
from PIL import Image
import time

#img_url = "https://lh3.googleusercontent.com/p/AF1QipMbZziubGkRy0Zjafrmpgvk9sN7dw9KlLBupQce=s680-w680-h510"
img_url = "https://www.google.com/search?q=drywall+chicago&sca_esv=583219155&rlz=1C1CHBF_enUS830US830&biw=1920&bih=931&tbm=lcl&ei=M-9YZZHGJYav0PEPubya2AQ&oq=drywall+chicago&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIg9kcnl3YWxsIGNoaWNhZ28qAggAMgUQABiABDIGEAAYFhgeMgYQABgWGB4yCBAAGBYYHhgPMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeSKo_UPcGWNUvcAJ4AJABAJgBf6AB0wmqAQM1Lje4AQHIAQD4AQHCAgsQABiABBiKBRiGA8ICCxAAGIAEGIoFGJECwgIHEAAYgAQYDcICChAAGIAEGIoFGEPCAg4QABiABBiKBRixAxiRAsICDhAAGIAEGIoFGMkDGJECwgILEAAYgAQYigUYkgPCAggQABiABBiSA8ICCBAAGIAEGLEDiAYB&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[41.9984806,-87.58136809999999],[41.7517225,-87.74741390000001]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"

options = Options()
options.add_experimental_option('detach',True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)


def get_images_from_google(url, driver):
    #def scroll_listings(driver):
    #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    driver.get(url) 
    
    time.sleep(3)

    #scroll_listings(driver)

    listings = driver.find_elements(By.CLASS_NAME,"dbg0pd")
    one_listing = listings[0]
    one_listing.click()
    print('clicked')
    print(len(listings))

    time.sleep(3)
#
    image_click = driver.find_elements(By.CLASS_NAME,"yOf5Ze")
    image_click[0].click()        
    print('clicked')
    #print(len(image_click))
    
    image_urls = []
    time.sleep(6)
    images = driver.execute_script("return document.getElementsByClassName('m7eMIc aQg20b')")
    print("Collecting Images")
    print(len(images))

    

    get_link_cmd = "return document.getElementsByClassName('m7eMIc aQg20b').item({0}).currentSrc"
    get_link_cmd2 = "return document.getElementsByClassName('m7eMIc aQg20b').item({0}).dataset['src']"

    for i in range(len(images)):
        if 'http' in driver.execute_script(get_link_cmd.format(i)):
            image_urls.append(driver.execute_script(get_link_cmd.format(i)))
            print("link captured")
        elif 'http' in driver.execute_script(get_link_cmd2.format(i)):
            image_urls.append(driver.execute_script(get_link_cmd2.format(i)))
            print("link captured")
#
    print(image_urls)

    temp_index = 126

    for i,url in enumerate(image_urls):
        download_image("C:\\Users\\alexp\\src\\ImgScrape\\img\\", url=url, file_name="picture{0}.jpg".format(temp_index))
        temp_index+=1
#


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

get_images_from_google(img_url,driver=driver)