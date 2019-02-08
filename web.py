from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
import io
import sys
import requests
import time
import json

try:
    driver = webdriver.Chrome()
except:
    print ("There's no ChromeDriver detected.Please install Chrome browser and proper ChromeDriver , then add their directory to PATH")
    exit()
else:
    try:
        fn=open("d://AutoIdleConfigName.conf","r")
    except IOError:
        print("This's no config detected.You are supposed to input your account and password")
        while(1):
            username = input("Here input your account name:")
            print("This is your username:",username,"\n Is it right ? Y/n ")        
            if(input()=='Y'):break
        while(1):
            password = input("Here input your password:")
            print("This is your password:",password,"\n Is it right? Y/n")
            if(input()=='Y'):break
        fn=open("d://AutoIdleConfigName.conf","w")
        fp=open("d://AutoIdleConfigPasswd.conf","w")
        fn.write(username)
        fp.write(password)
        fn.close()
        fp.close()
    else:
        fp=open("d://AutoIdleConfigPasswd.conf","r")
        username=fn.read()
        password=fp.read()
        print("Your username:",username,"\nYour password:",password)
        fn.close()
        fp.close()

url = "http://lawyeredu.pkulaw.cn/index.php"
driver.get(url)
print("Webpage loaded")

username_web= driver.find_element_by_id("top_username")
print("Username filled")
username_web.send_keys(username)
time.sleep(1)

userpasswd_web= driver.find_element_by_id("top_password")
print("Password filled")
userpasswd_web.send_keys(password)

driver.execute_script("bfa_login()")
print("Login successfully")

time.sleep(2)
url = "http://lawyeredu.pkulaw.cn/index.php?m=member&c=aclaedu&a=mycourse&t=4"
driver.get(url)

table=driver.find_element_by_class_name("table-1")
table_rows = table.find_elements_by_tag_name('tr')
table_cols = table_rows[0].find_elements_by_tag_name('th')
for i in range(1,len(table_rows)):
    if((table_rows[i].find_elements_by_tag_name('td')[3].text) == "100%"):
        table_rows[i].find_elements_by_tag_name('td')[0].click()
        allHandles = driver.window_handles
        driver.close()
        driver.switch_to.window(allHandles[1])
        driver.find_element_by_class_name("show_scorm_button").click()
        allHandles = driver.window_handles
        driver.close()
        driver.set_page_load_timeout(15)
        while(1):
            try:
                driver.switch_to.window(allHandles[1])
                time.sleep(5)
                print("open play page successfully")
                percent = driver.find_element_by_id("cpl")
                print("Trying to tackle the exception")
                print("该课程的完成百分比为：",percent)
                break
            except TimeoutException:
                print("time out after 15 seconds when loading page")
                driver.execute_script("window.stop()")
                driver.refresh()
            except:
                a1 = Alert(driver)
                a1.accept()
        break
    else: print ("课程： " ,table_rows[i].find_elements_by_tag_name('td')[0].text , " 已学习完毕")
print ("所有课程学习完毕。")
#driver.save_screenshot('picture4.png')
