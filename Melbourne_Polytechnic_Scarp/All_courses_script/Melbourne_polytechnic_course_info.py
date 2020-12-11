"""Description:
    * author: Sayem Rahman
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 09-12-20
    * description:This script extracts all the courses links and save it in txt file.
"""

import copy
import csv
import json
import re
import time
from pathlib import Path
import ast
# noinspection PyProtectedMember
from bs4 import Comment
from selenium import webdriver
from CustomMethods import DurationConverter, TemplateData
import bs4 as bs4
import requests
import os
from CustomMethods import DurationConverter as dura, DurationConverter
from CustomMethods import TemplateData


def tag_text(tag):
    return tag.get_text().__str__().strip()


def parseint(string):
    m = re.search(r"(\d*\.?\d*)", string)
    return m.group() if m else None


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/test_links.txt'
#course_links_file_path = course_links_file_path.__str__() + '/Melbourne_polytechnic_course_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/Melbourne_polytechnic_courses_info.csv'

course_data_all = []

possible_cities = {'Preston': 'Melbourne',
                   'Fairfield': 'Sydney',
                   'Epping': 'Melbourne',
                   'Heidelberg': 'Melbourne',
                   'Greensborough': 'Melbourne',
                   'Prahran': 'Melbourne',
                   'Collingwood': 'Melbourne'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    course_data = {'Level_Code': '',
                   'University': 'Melbourne Polytechnic',
                   'City': '',
                   'Course': '',
                   'Faculty': '',
                   'Int_Fees': '',
                   'Local_Fees': '',
                   'Free TAFE': '',
                   'Job Trainer': '',
                   'Concession': '',
                   'Government subsidised fee': '',
                   'Non-subsidised fee': '',
                   'Currency': 'AUD',
                   'Currency_Time': 'Years',
                   'Course_Delivery_Mode': 'Normal',
                   'Duration': '',
                   'Duration_Time': 'Year(s)',
                   'Full_Time': '',
                   'Part_Time': '',
                   'Prerequisite_1': 'Year 12',
                   'Prerequisite_2': 'IELTS',
                   'Prerequisite_3': 'ATAR ',
                   'Prerequisite_1_grade_1': '',
                   'Prerequisite_2_grade_2': '',
                   'Prerequisite_3_grade_3': '',
                   'Website': '',
                   'Course_Lang': 'English',
                   'Availability': 'A',
                   'Description': '',
                   'Career_Outcomes/path': '',
                   'Country': 'Australia',
                   'Online': '',
                   'Offline': '',
                   'Distance': '',
                   'Face_to_Face': '',
                   'Blended': '',
                   'Remarks': ''}

    actual_cities = []

    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # # SAVE COURSE TITLE

    print(pure_url)

    title = soup.select('.course-hero__text > h1:nth-child(1)')
    course_info = []
    for t in title:
        course_title = tag_text(t)
        course_title = ' '.join(course_title.split())
        # course_info.append(course_title)
        # print(course_title)
        # course_title = get_course_title()

    course_data['Course'] = course_title

    print(course_data['Course'])

# DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    #print(course_data['Level_Code'])

# DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i
    #print(course_data['Faculty'])

# # COURSE DESCRIPTION
    #desc = soup.select('div.course-overview__text:nth-child(3) > p:nth-child(2)')
    desc = soup.select('div.course-overview__text:nth-child(3)')

    for d in desc:
        course_description = tag_text(d).replace('\n', ' .')
        #print(course_description)
        course_data['Description'] = course_description
    #print(course_data['Description'])


# CAREER OUTCOME
    try:
        outcome = soup.select('ul.multi-col:nth-child(3)')
        for o in outcome:
            c_outcome = tag_text(o).replace('\n', '/ ')
            course_data['Career_Outcomes/path'] = c_outcome
            #print(c_outcome)

    except AttributeError:
        course_data['Career_Outcomes/path'] = ""
        #print("No career Outcomes for", course_data['Course'])

#DURATION/Duration Time/FullTime/Parttime/

    avaialbility_list = []

    try:
        duration = soup.select("div.course-overview__info:nth-child(3) > div:nth-child(2) > p:nth-child(1)")
        for t in duration:
            dur = tag_text(t)
            # print(dur)
            course_duration = DurationConverter.convert_duration((dur))
            # print(course_duration)
            course_data['Duration'] = course_duration[0]
            course_data['Duration_Time'] = course_duration[1]
    except TypeError:
        course_data['Duration'] = 'N/A'
        course_data['Duration_Time'] = 'N/A'
    # print(course_data['Duration'])
    # print(course_data['Duration_Time'])

    avaialbility_list.append(dur)

    for data in avaialbility_list:
        if avaialbility_list:

            if data.lower().find('full-time') != -1 and data.lower().find('part-time') != -1:
                course_data['Part_Time'] = 'Yes'
                course_data['Full_Time'] = 'Yes'
            elif data.lower().find('full time') != -1 or data.lower().find('full-time') != -1:
                course_data['Full_Time'] = 'Yes'
                course_data['Part_Time'] = ''
            elif data.lower().find('part time') != -1 or data.lower().find('part-time') != -1:
                course_data['Part_Time'] = 'Yes'
                course_data['Full_Time'] = ''

        else:
            course_data['Part_Time'] = ''
            course_data['Full_Time'] = ''

    # BLENDED/ FACE TO FACE/ ONLINE
    delivery = soup.select("ul.multi-col:nth-child(4)")
    delivery2 = soup.select("ul.multi-col:nth-child(9)")

    avaialbility_list = ''
    for t in delivery:
        c_delivery = tag_text(t)
        avaialbility_list = avaialbility_list + c_delivery
    for f in delivery2:
        c_delivery2 = tag_text(f)
        avaialbility_list = avaialbility_list + c_delivery2

    avaialbility_list = avaialbility_list.split('\n')
    print(avaialbility_list)

    # print(delivery)
    # avaialbility_list = ''
    # for t in delivery:
    #     c_delivery = tag_text(t)
    #     avaialbility_list = avaialbility_list + c_delivery
    #
    # avaialbility_list = avaialbility_list.split('\n')
    # print(avaialbility_list)

    for data in avaialbility_list:
        if 'online' in data.lower():
            course_data['Online'] = 'Yes'
        if 'virtual' in data.split():
            #online = re.findall('\\bvirtual\\b', data)
            #if online != 0:
            course_data['Online'] = 'Yes'
        if 'blended' in data.lower():
            course_data['Blended'] = 'Yes'
        if 'face-to-face' in data.lower():
            course_data['Offline'] = 'Yes'
        if 'practical' in data.lower():
            course_data['Offline'] = 'Yes'
        if 'remote' in data.lower():
            course_data['Offline'] = 'Yes'
        if 'classroom' in data.lower():
            #offline = re.findall('\\bclassroom\\b', data)
            #if offline != 0:
            course_data['Offline'] = 'Yes'
        if 'onsite' in data.lower():
            course_data['Offline'] = 'Yes'
        if 'Apprenticeship' in data.lower():
            course_data['Course_Delivery_Mode'] = 'Apprecticeship'
        if 'Traineeship' in data.lower():
            course_data['Course_Delivery_Mode'] = 'Apprecticeship'

    # print("Online :", course_data['Online'])
    # print("Offline :", course_data['Offline'])
    # print("Blended :", course_data['Blended'])

# ALL DOMESTIC FEES
    # TYPE 1: WEBSITES THAT CONTAINS FROM 2 TO 5 TYPES OF FEES(free TAFE, Trainer Fee, Concession, )
    # Finding the fee types
    table_rows = soup.select(
        '.course-fees > div:nth-child(3) > div:nth-child(1) > table:nth-child(1) > thead:nth-child(1) > tr:nth-child(1)')
    table_rows_list = ''
    feeCatagory = []
    for t in table_rows:
        rows = t.find_all('th')
        for header in rows:
            header = tag_text((header)).split('\n')
            header = header.pop(0)
            feeCatagory.append(header)
    # print(feeCatagory)

    # Finding the fees of different type
    fees = soup.select('.course-fees > div:nth-child(3) > div:nth-child(1)')
    # print(fees)
    listed_fee = {}
    feeList = []
    for fee in fees:
        payable = fee.find_all('b')
        # print(payable)
        index = 1

        for p in payable:
            pay = tag_text((p))
            # print(pay)
            # print(index)
            pay_amount = 0
            if '$' in pay:
                pay_amount = pay.replace('$', '').replace(' ', '')
                # print(pay_amount)
                feeList.append(pay_amount)
                course_data[feeCatagory[index]] = pay_amount
                index += 1

    ## Type 2 fess (website containing only per year and semester fee)
    # if course_data['Local_Fees'] is None:
    try:
        table_rows3 = soup.select('.course-fees > div:nth-child(2)')
        for fee in table_rows3:
            fees = fee.find('td').find_next('td')
            fees = tag_text(fees).replace('$', '').replace(' ', '')
            course_data['Local_Fees'] = fees
            #print("Type 3 Fee :", course_data['Local_Fees'])

    ## FOR TYPE 3 WEBSITE THAT HAS FEE ON THE RIGHT TOP

        table_rows2 = soup.find_all('p', class_='mp-course-fees__amount')
        for fee in table_rows2:
            fees = tag_text(fee).replace('$', '').replace(' ', '')
            course_data['Local_Fees'] = fees
            course_data['Int_Fees'] = fees
            print(fees)

        #print("Type 2 Fee", course_data['Local_Fees'])

    except Exception:
        print("")

    # print("lsitedFees :",listed_fee)
    # print(feeList)
    # print(course_data)

# INTERNATIONAL FEE

    try:
        int_fees2 = browser.find_elements_by_class_name('standard__table')
        for fee in int_fees2:
            full_fee = fee.find_element_by_xpath('/html/body/div[2]/div[3]/div[4]/div[2]/section[6]/div/div/div/div[3]/div/table/tbody/tr[1]/td[2]').text
            full_fee = full_fee.replace('$', '')
            #full_fee = ''.join([n for n in full_fee if n.isdigit()])
            course_data['Int_Fees'] = full_fee
            #print("international Fee1:",full_fee)

    except Exception:
        pass


# PREREQUISITE 1 (YEAR 12)
    try:
        pre_1 = browser.find_elements_by_class_name('container__col')
        for required in pre_1:
            requirements = required.find_element_by_xpath('/html/body/div[2]/div[3]/div[4]/div[2]/section[8]/div/div/span[2]').text
            requirements = requirements.split()
            try:
                year = requirements[requirements.index('Year') + 1]
                course_data['Prerequisite_1_grade_1'] = year
                #print(year)
                print('Year grade',course_data['Prerequisite_1_grade_1'])
            except Exception:
                course_data['Prerequisite_1_grade_1'] = ''
    except Exception:
        course_data['Prerequisite_1_grade_1'] = ''

# PREREQUISITE 2 (IELTS)

    try:
        pre_2 = browser.find_elements_by_class_name('container__col')
        for required in pre_2:
            requirements = required.find_element_by_xpath('/html/body/div[2]/div[3]/div[4]/div[2]/section[8]/div/div/span[2]').text
            requirements = requirements.split()
            try:
                ielts = requirements[requirements.index('IELTS') + 1]
                ielts_score = '.'.join([n for n in ielts if n.isdigit()])
                course_data['Prerequisite_2_grade_2'] = ielts_score
                #print(ielts)
                print('IELTS SCORE' ,course_data['Prerequisite_2_grade_2'])
            except Exception:
                course_data['Prerequisite_2_grade_2'] = ''
    except Exception:
        course_data['Prerequisite_1_grade_1'] = ''

# PREREQUISITE 3 (ATAR)

    try:
        pre3 = soup.select('section.mp-standard-text:nth-child(15) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)')
        for required in pre3:
            required = tag_text(required)
            r = re.compile("ATAR(.*)")
            requirements = (r.findall(required))
            requirements  = ''.join(map(str, requirements))     #convert to string
            requirements = re.findall(r'\d+', requirements)
            atar = int(''.join(str(i) for i in requirements))
            if atar >= 40:
                course_data['Prerequisite_3_grade_3'] = atar
                print("Atar Score:", atar)
            else:
                course_data['Prerequisite_3_grade_3'] = ''

    except Exception:
        course_data['Prerequisite_3_grade_3'] = ''

    print(course_data)
# # DUPLICATE ENTRIES with multiple cities for each city
#     for i in actual_cities:
#         course_data['City'] = possible_cities[i]
#         course_data_all.append(copy.deepcopy(course_data))
#     del actual_cities
#
#     # print(course_data)
#     temp = course_data.copy()
#     course_data_all.append(temp)
#
#
# # TABULATE OUR DATA
# desired_order_list = ['Level_Code',
#                       'University',
#                       'City',
#                       'Course',
#                       'Faculty',
#                       'Int_Fees',
#                       'Local_Fees',
#                       'Free TAFE',
#                       'Job Trainer',
#                       'Concession',
#                       'Government subsidised fee',
#                       'Non-subsidised fee',
#                       'Currency',
#                       'Currency_Time',
#                       'Course_Delivery_Mode',
#                       'Duration',
#                       'Duration_Time',
#                       'Full_Time',
#                       'Part_Time',
#                       'Prerequisite_1',
#                       'Prerequisite_2',
#                       'Prerequisite_3',
#                       'Prerequisite_1_grade_1',
#                       'Prerequisite_2_grade_2',
#                       'Prerequisite_3_grade_3',
#                       'Website',
#                       'Course_Lang',
#                       'Availability',
#                       'Description',
#                       'Career_Outcomes/path',
#                       'Country',
#                       'Online',
#                       'Offline',
#                       'Distance',
#                       'Face_to_Face',
#                       'Blended',
#                       'Remarks']
#
#
#
#
# with open(csv_file, 'w', encoding='utf-8', newline='\n') as output_file:
#     dict_writer = csv.DictWriter(output_file, desired_order_list)
#     dict_writer.writeheader()
#     for course in course_data_all:
#         dict_writer.writerow(course)
#
#
# with open(csv_file, 'r', encoding='utf-8') as infile, open('Melbourne_Polytechnic_courses_ordered.csv', 'w', encoding='utf-8',
#                                                            newline='') as outfile:
#     writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
#     # reorder the header first
#     writer.writeheader()
#     for row in csv.DictReader(infile):
#         # writes the reordered rows to the new file
#         writer.writerow(row)
