"""Description:
    * author: Sayem Rahman
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 09-12-20
    * description:This script extracts all the courses links and save it in txt file.
"""

from pathlib import Path
from urllib.parse import urljoin
import os
import requests
import bs4
import bs4 as bs4
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
import re
import time
# selenium web driver
# we need the Chrome driver to simulate JavaScript functionality
# thus, we set the executable path and driver options arguments
# ENSURE YOU CHANGE THE DIRECTORY AND EXE PATH IF NEEDED (UNLESS YOU'RE NOT USING WINDOWS!)

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)



# MAIN ROUTINE
courses_page_url = 'https://www.melbournepolytechnic.edu.au/search/?studentType=0&query=&activeTab=0&page='
list_of_links = []

delay_ = 5  # seconds


# EXTRACT ALL THE LINKS TO LIST

def fetch_url(courses_page_url):
    print(courses_page_url)
    browser.get(courses_page_url)
    result_elements = browser.find_elements_by_class_name('mp-search-entry')
    for element in result_elements:
        a_tag = element.find_element_by_tag_name('a')
        link = a_tag.get_property('href')
        list_of_links.append(link)
        #print(link)


#iterate through all the pages
for i in range(1, 13):
    # url = url + str(i)
    fetch_url(courses_page_url + str(i))

print(*list_of_links, sep='\n')



# SAVE LINKS TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/Melbourne_polytechnic_course_links.txt'
course_links_file = open(course_links_file_path, 'w')

# print(course_links)
for i in list_of_links:
    print(i)
    # print(i.strip())
    # course_links_file.write(i.strip() + '\n')
    if i is not None and i != "" and i != "\n":
        if i == list_of_links[-1]:
            course_links_file.write(i.strip())
        else:
            course_links_file.write(i.strip()+'\n')
course_links_file.close()