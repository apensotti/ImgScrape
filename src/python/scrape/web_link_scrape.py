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
img_url = "https://www.google.com/search?sca_esv=583219155&rlz=1C1CHBF_enUS830US830&tbs=lf:1,lf_ui:2&tbm=lcl&sxsrf=AM9HkKnqKGJXMBORN3ngDEAKr3o6NZjmyw:1700189717482&q=drywall+boulder&rflfq=1&num=10&sa=X&ved=2ahUKEwi01aShhMqCAxWMomoFHd6EBkEQjGp6BAgfEAE&biw=1920&bih=931&dpr=1#rlfi=hd:;si:8732774125950856829,l,Cg9kcnl3YWxsIGJvdWxkZXJI76ulmOaAgIAIWhcQABgAGAEiD2RyeXdhbGwgYm91bGRlcnoHQm91bGRlcpIBE2RyeV93YWxsX2NvbnRyYWN0b3KaASRDaGREU1VoTk1HOW5TMFZKUTBGblNVUjVOWEo1WkRoM1JSQUKqAVoKCS9tLzAxd19wNwoIL20vMG5jajgQASoLIgdkcnl3YWxsKAAyHxABIhsvpyVJ9PE3-OaLQsqImDJLFWPGKLuFXgWfxKwyExACIg9kcnl3YWxsIGJvdWxkZXLgAQA;mv:[[40.08554743245166,-105.16690212424315],[39.98223956754832,-105.33289867575681]]"

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
    one_listing = listings[7]
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

    temp_index = 72

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