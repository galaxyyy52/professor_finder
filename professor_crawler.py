from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from itertools import repeat
import json

major_list = [
    {
        'dept': 'ece',
        'url': '/about/directory/faculty-dept'
    },
    {
        'dept': 'cs',
        'url': '/about/people/all-faculty/department-faculty'
    },
    {
        'dept': 'matse',
        'url': '/people/faculty/department-faculty'
    },
    {
        'dept': 'mechse',
        'url': '/people/faculty'
    },
    {
        'dept': 'aerospace',
        'url': '/directory/faculty/faculty-members'
    },
    {
        'dept': 'cee',
        'url': '/directory/faculty/all-faculty'
    },
    {
        'dept': 'chbe',
        'url': '/directory/faculty/all-faculty'
    },
    {
        'dept': 'bioengineering',
        'url': '/people/faculty'
    },
    {
        'dept': 'ise',
        'url': '/directory/faculty'
    }
]

def get_prof_brief(home_page_url):
    browser.get(home_page_url)
    page_text_prof = browser.page_source
    soup_prof = BeautifulSoup(page_text_prof, 'lxml')
    research_area_obj = soup_prof.select('.extProfileAREA > ul > li')
    research_area = []
    for i in research_area_obj:
        research_area.append(i.text)
    courses_obj = soup_prof.select('.extProfileCourses > ul > li')
    courses_taught = []
    for i in courses_obj:
        courses_taught.append(i.text)

    return research_area, courses_taught

def prof_index(faculty_url, department):
    browser.get(faculty_url)
    page_text = browser.page_source
    soup = BeautifulSoup(page_text, 'lxml')

    faculty_list = soup.select('.directory-list-4 > div')

    professor_list = []
    for faculty in faculty_list:
        photo_url = 'https://' + faculty.find('div', class_='photo')['style'][24:-1]
        home_page_url = dept_url + faculty.select('.name > a')[0]['href']
        research_area, courses_taught = get_prof_brief(home_page_url)
        professor = {
            'name': faculty.select('.name > a')[0].text,
            'department': department,
            'photo_url': photo_url,
            'home_page_url': home_page_url,
            'doc_name': faculty['data-experts-key'],
            'brief': {
                'title': faculty.find('div', class_='title').text,
                'research_area': research_area,
                'courses_taught': courses_taught
            }
        }
        professor_list.append(professor)

    return professor_list


def write_index(professor_list):
    json_str = json.dumps(professor_list, indent=4)
    # print(json_str)
    file = open("professor_index.json", "a")
    file.write(json_str)


def prof_doc(professor_list):
    for professor in professor_list:
        browser.get(professor['home_page_url'])
        page_text_prof = browser.page_source
        soup_prof = BeautifulSoup(page_text_prof, 'lxml')
        page_text = soup_prof.find('div', id='content_inner').text
        file = open("./professor_doc/" + professor['name'] + ".txt", "w", encoding="utf-8")
        file.write(page_text)


if __name__ == '__main__':
    browser = webdriver.Chrome(executable_path='./chromedriver.exe')
    for major in major_list:
        department = major['dept']
        dept_url = 'https://' + department + '.illinois.edu'
        faculty_url = dept_url + major['url']

        professor_list = prof_index(faculty_url, department)
        write_index(professor_list)
        prof_doc(professor_list)

        browser.close()


