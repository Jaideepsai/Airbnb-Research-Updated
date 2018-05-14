
# coding: utf-8

# In[1]:


# Scrapping works only for images from AIrbnb http://insideairbnb.com/get-the-data.html excel
import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/jaideepsai/Downloads/512_listings.csv")
df = pd.DataFrame(data)[185:]
#df


# In[2]:


import urllib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import time
try:
    if not os.path.exists('ScrappedImages-520-listings'):
        os.makedirs('ScrappedImages-520-listings')
except OSError:
    print ('Error: Creating directory of data')


# In[3]:


#works in mac only and only for airbnb listings url 
#scrapped images from  the slide show for each airbnb listing
options = webdriver.ChromeOptions()
#changes for windows and mac
options.binary_location = 'C:\Users\jaideepsai\AppData\Local\Google\Chrome SxS\Application\chrome.exe'
#options.add_argument('window-size=800x841')
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
options.add_argument('--enable-gpu')
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Chrome("C:\Users\jaideepsai\Downloads\chromedriver.exe")
chrome_driver_path ="C:\Users\jaideepsai\Downloads\chromedriver.exe"
sum_total=0
count_listings=0
for row in df.itertuples():
    print(row[1])
    data_url="https://www.airbnb.com/rooms/"+str(row[1])
	
    time.sleep(np.random.randint(1,10))
    driver.get(data_url)
    try:
        time.sleep(np.random.randint(1,2))
        #class keeps updating in airbnb site need to check constantly
        driver.find_element_by_css_selector('._1s8f7pz').click()
        num=driver.find_element_by_css_selector('._dxgq4v').text.split(':')[0].split('/')[1]
        int_num=int(num)
        sum_total=sum_total+int_num
        count_listings=count_listings+1
        print "total "+str(int_num)+" images-"+str(row[2])
        count = 0
        while (count < int_num):
            image_v=""
            try:
                driver.find_element_by_xpath("//*[@class='text-muted']").text;
                image_v="_verified";
            except:
                image_v=""; 
            topLinks = driver.find_element_by_class_name('Slideshow__images')
            botLink=topLinks.find_element_by_tag_name('img')
            image=botLink.get_attribute("src")
            print(botLink.get_attribute("src"))
            urllib.urlretrieve(image, "./ScrappedImages-520-listings/"+data_url.split('/rooms/')[1]+'_'+str(count)+image_v+".png")
            time.sleep(np.random.randint(1,2))
            driver.find_element_by_css_selector('._elqfm6c').click()
            count = count + 1
    except NoSuchElementException:
        print data_url + " listing is no longer available."
print "total sum "+str(sum_total)+" images and "+ str(count_listings)+" active listings out of "+str(len(df))
driver.quit()
