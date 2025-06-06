import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)  # Adjust this path according to your directory structure
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_jwt.settings')  # Adjust to your project name

import django

django.setup()  # Update Django configuration

import json
import random
from datetime import datetime
from hashlib import md5
import variables
import requests
from bs4 import BeautifulSoup
from lingxi_main.items.CrawledDocItem import CrawledDocItem
from lingxi_main.crud.save_contents import save_CrawledDocs  # Import the function here
from django_my_jwt.utils.util_tools import get_num_range_from_text,get_num_range_from_text
import math
import re

MAX_PAGE = 3

def convert_p_tags_to_newlines_and_remove_html(html_content):
    # Remove opening <p> tags
    content_with_newlines = re.sub(r'<p>', '', html_content)
    # Replace all occurrences of one or more </p > tags with exactly 2 newline characters
    content_with_newlines = re.sub(r'(</p >)+', '\n\n', content_with_newlines)
    # Remove any remaining HTML tags
    content_with_newlines = re.sub(r'<[^>]+>', '', content_with_newlines)
    # Remove any extra newlines at the beginning and end
    content_with_newlines = content_with_newlines.strip()
    return content_with_newlines

def get_random_user_agent(file_path):
    with open(file_path, 'r') as file:
        user_agents = file.readlines()
    return random.choice([ua.strip() for ua in user_agents if ua.strip()])


def fetch_page():
    base_url = 'https://www.yeeyi.com/classified-advertisement/au/{}/{}/'
    user_agent_file_path = variables.root_path + "/data/crawler_config/user_agents.txt"
    user_agent = get_random_user_agent(user_agent_file_path)
    headers = {
        'User-Agent': user_agent
    }
    #81294  'sydney',
    cities = [ 'sydney','melbourne','canberra', 'adelaide', 'perth', 'darwin','brisbane', 'hobart','central-coast', 'geelong', 'ballarat', 'gold-coast',
              'wollongong', 'others' ]  # Add more cities as needed
    categories = ['property-rent','supermarkets', 'jobs', 'car-sale', 'marketplace', 'textbooks', 'pets-sale',
                  'property-sale', 'business-sale']
    category_mapping = {
        'property-rent': ('rent_house', 23, None, None),
        'supermarkets': ('others', 25, None, None),  # No direct match, categorize as 'others'
        'jobs': ('job', 14, None, None),
        'car-sale': ('secondhand_trading', 21, 'car', 2101),
        'marketplace': ('secondhand_trading', 21, None, None),
        # Assuming general marketplace falls under secondhand trading
        'textbooks': ('secondhand_trading', 21, 'book', 2102),
        'pets-sale': ('pet', 19, None, None),
        'property-sale': ('buy_house', 22, None, None),
        'business-sale': ('run_business', 15, None, None)
    }

    for city in cities:
        for category in categories:
            try:
                response = requests.get(base_url.format(city, category), headers=headers)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                print(f'Response Status Code for {city} - {category}:', response.status_code)

                # Parse the HTML response content
                soup = BeautifulSoup(response.text, 'html.parser')

                script_tag = soup.find('script', id='__NEXT_DATA__')
                if script_tag:
                    # Extract the JSON-like content from the script tag
                    script_content = script_tag.string

                    # Load the JSON content
                    data = json.loads(script_content)

                    # Navigate through the JSON data to find the required information
                    page_props = data.get('props', {}).get('pageProps', {})

                    filters = page_props.get('filters', {})
                    city_filter = filters.get('cityFilter')
                    fid = page_props.get('fid')
                    total_list_count = page_props.get('total_list_count')
                    if total_list_count is not None:
                        page_number = math.ceil(int(total_list_count) / 45)
                        page_number = min(page_number,MAX_PAGE)
                    else:
                        page_number = 1

                else:
                    print("Script tag with id '__NEXT_DATA__' not found.")


                if script_tag:
                    tid_values = set()
                    json_data = json.loads(script_tag.string)
                    # Extract tid values
                    page_data = json_data.get('props', {}).get('pageProps', {}).get('pageData', [])
                    #page_data = page_props.get('pageData', [])
                    for item in page_data:
                        if 'tid' in item:
                            tid_values.add(item['tid'])


                    if page_number > 2:
                        headers = {
                            'User-Agent': user_agent
                        }
                        for page in range(2, page_number + 1):
                            json_data = {
                                'fid': fid,
                                'nextPage': page,
                                'start': 0,
                                'cityFilter': city_filter,
                                'devid': 'ebd32e8-c502-83c3-e63-a403fe5eaf6|pc',
                            }
                            response = requests.post('https://www.yeeyi.com/api/getSectionList/', headers=headers,
                                                     json=json_data)
                            response_json = response.json()
                            thread_list = response_json.get('threadlist',{})

                            for thread in thread_list:
                                if 'tid' in thread:
                                    tid_values.add(thread['tid'])
                                    # print("tid_values : ",tid_values)

                                print(f'Extracted TID values for {city} - {category}:')
                                for tid in tid_values:
                                    fetch_tid_page(tid, city, category,category_mapping[category], headers)
                                tid_values = set()
                else:
                    print(f'Could not find JSON data in the response for {city} - {category}.')

            except requests.exceptions.HTTPError as http_err:
                print(f'HTTP error occurred for {city} - {category}: {http_err}')
            except Exception as err:
                print(f'Other error occurred for {city} - {category}: {err}')


def fetch_tid_page(tid, city, category,mapped_category_tuple, headers):
    tid_url = f'https://www.yeeyi.com/classified-advertisement/au/{city}/{category}/{tid}/'
    try:
        response = requests.get(tid_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        # Find the script tag with id __NEXT_DATA__
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

        # Parse the JSON content
        json_data = json.loads(script_tag.string)

        # Extract the title
        section_3_content = json_data['props']['pageProps']['houseRentDetails']['threadInfo']['section_3']
        section_2_content = json_data['props']['pageProps']['houseRentDetails']['threadInfo']['section_2']

        title = section_2_content['subject']
        pic_urls = [item['picUrl'] for item in
            json_data['props']['pageProps']['houseRentDetails']['threadInfo']['section_1']]
        content = json_data['props']['pageProps']['houseRentDetails']['threadInfo']['section_4']
        html_content_for_content = content.get('message', "")
        soup_for_content = BeautifulSoup(html_content_for_content, 'html.parser')
        text_content = soup_for_content.get_text()
        publication_date_timestamp = json_data['props']['pageProps']['houseRentDetails']['threadInfo']['section_2']['dateline']
        author_name = section_2_content['author']
        author_url = 'https://yeeyi.com/user/profile/'+ section_2_content['authorid']
        city_related = city
        contact= section_2_content.get('tel', 'No tel found')
        publication_date = datetime.fromtimestamp(int(publication_date_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now()
        address = section_2_content.get('address')

        likes = section_2_content.get('likes')
        if likes is None:
            likes = 0
        comments_cnt = section_2_content.get('replies')
        views = section_2_content.get('views')

        # Extract only the date partprint(section_2_content)
        #         print(section_3_content)
        #         # Extract only the date part
        #         update_date = current_datetime.date()
        update_date = current_datetime.date()
        # price
        price_text = ""
        for item in section_3_content:
            if item[0] == '价格' and item[1]:
                price_text = item[1]
                break
        for item in section_3_content:
            if item[0] == '工资待遇' and item[1]:
                price_text = item[1]
                break
        house_rents = section_2_content.get('house_rents')
        if house_rents:
            try:
                price_text = str(house_rents)
            except (ValueError, AttributeError):
                price_text = ""
        #price
        #job
        #print(section_3_content)
        company_name = ""
        for item in section_3_content:
            if item[0] == '公司名称' and isinstance(item[1], str):
                company_name= str(item[1])
                break
        job_title = ''
        for item in section_3_content:
            if item[0] == '招聘职位' and isinstance(item[1], str):
                job_title = str(item[1])
                break
        job_type = ''
        for item in section_3_content:
            if item[0] == '工作性质' and isinstance(item[1], str):
                job_type = str(item[1])
                break
        requirement = ''
        for item in section_3_content:
            if item[0] == '学历要求' and isinstance(item[1], str):
                requirement = str(item[1])
                break
        job_classification = ''
        for item in section_3_content:
            if item[0] == '招聘职位' and isinstance(item[1], str):
                job_classification = str(item[1])
                break
        extracted_data = {
            'annual_leave': None,
            'superannuation': None,
            'recruitment_count': None,
            'visa_status': None
        }

        # Extract the values
        for item in section_3_content:
            if item[0] == 'Annual leave':
                extracted_data['annual_leave'] = item[1]
            elif item[0] == 'Superannuation':
                extracted_data['superannuation'] = item[1]
            elif item[0] == '招聘人数':
                extracted_data['recruitment_count'] = item[1]
            elif item[0] == '签证状态':
                extracted_data['visa_status'] = item[1]

        blog_url = tid_url
        blog_location = None
        for item in section_3_content:
            if item[0] == "所在地区":
                blog_location = item[1]

        nested_content = convert_p_tags_to_newlines_and_remove_html(content['message'])


        min_price = get_num_range_from_text(price_text)[0]
        max_price = get_num_range_from_text(price_text)[1]
        doc_id = md5(blog_url.encode('utf-8')).hexdigest()
        main_cat, main_cat_id, sub_cat, sub_cat_id = mapped_category_tuple
        crawled_doc_item = CrawledDocItem()
        crawled_doc_item.doc_id = doc_id
        crawled_doc_item.query = ''
        crawled_doc_item.website = 'yeeyi'
        crawled_doc_item.blog_url = blog_url
        crawled_doc_item.author_name = author_name
        crawled_doc_item.author_url = author_url
        crawled_doc_item.title = title
        crawled_doc_item.title_chn = title
        crawled_doc_item.content =  repr(nested_content)
        crawled_doc_item.content_chn = text_content
        crawled_doc_item.publish_date = publication_date
        crawled_doc_item.blog_location = blog_location
        crawled_doc_item.imgs_url = ',,,'.join(pic_urls)
        crawled_doc_item.status = 0
        crawled_doc_item.city_related = city_related
        crawled_doc_item.blog_text_type = '正常帖'
        crawled_doc_item.video_src=""
        crawled_doc_item.address = address
        crawled_doc_item.job_points = extracted_data
        crawled_doc_item.comments_cnt = comments_cnt
        crawled_doc_item.like_cnt =likes
        crawled_doc_item.collect_cnt = views
        crawled_doc_item.big_cat=main_cat
        crawled_doc_item.min_price = int(min_price)
        crawled_doc_item.max_price = int(max_price)
        crawled_doc_item.cat_name1= sub_cat if sub_cat else ''
        crawled_doc_item.cat_id1 = sub_cat_id if sub_cat_id else main_cat_id
        crawled_doc_item.country_related="australia"
        crawled_doc_item.contacts = contact
        crawled_doc_item.wrt_pt=update_date
        crawled_doc_item.job_company = company_name
        crawled_doc_item.job_required_features = requirement
        crawled_doc_item.job_title = job_title
        crawled_doc_item.job_title_chn = job_title
        crawled_doc_item.job_classification = job_classification
        crawled_doc_item.job_type = job_type
        crawled_doc_item.price_text = price_text

        print("----准备写入: ",crawled_doc_item.doc_id)
        save_CrawledDocs(crawled_doc_item)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred for TID {tid}: {http_err}')
    except Exception as err:
        print(f'Other error occurred for TID {tid}: {err}')

if __name__ == "__main__":
    fetch_page()