import requests
import re
import json
import os
import time
import threading


class CourseScraper:

    def __init__(self, exportdir):
        self.export_dir = exportdir
        self.base_url = "https://w2prod.sis.yorku.ca"
        self.course_url = "https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm"

    def get_course_root_site(self):
        '''
        Returns the root Yorku courses site
        '''

        page = requests.get(self.course_url)
        return page.text

    def get_search_by_faculty_url(self, site_html):
        '''
        Takes url of the root site and returns the url of the search by faculty page
        '''
        find_str = r'<a href="/Apps/WebObjects/cdm.woa/.*">Subject</a>'
        found_result = re.search(find_str, site_html)
        text = found_result.group(0)
        return text.replace(r'<a href="', '').replace(r'">Subject</a>', '')

    def get_links_from_by_faculty_page(self, site_html):
        '''
        Extracts the links to the by faculty pages
        '''

        # first look for the url to submit the html post form
        find_form_url = r'<form name="subjectForm" method="post" action="([\w\W]+[0-9])">' + \
            "\n\t\t\t<P></P>"
        found_result = re.search(find_form_url, site_html)

        form_url = found_result.group(1)

        # then scrape all of the subjects/faculties appearing in the page
        find_subjects = r'value="([0-9]+)">(\w+) +- (\w+)'
        found_result = re.findall(find_subjects, site_html)
        subjects = []
        for f in found_result:
            subjects.append((int(f[0]), f[1]))

        # also scrape the available sessions (fall/winter/summer)
        sessions = [0, ]

        # there is also a hidden field called wosid,
        find_wosid = r'<input type="hidden" name="wosid" value="([\w\W]+)">'
        found_result = re.search(find_wosid, site_html)

        #form_wosid = text.replace(r'<input type="hidden" name="wosid" value="', '').replace(r'">', '')
        form_wosid = found_result.group(1)
        form_wosid = form_wosid[:22]

        return {"form_url": form_url, "sessions": sessions, "subjects": subjects, "wosid": form_wosid}

    def get_list_page(self, faculty_page_attrs, subject, session=0):
        '''
        Returns dict containing subject info
        look at the select menu for the subjects
        '''
        return requests.post(
            faculty_page_attrs["form_url"],
            data={
                "sessionPopUp": session,
                "subjectPopUp": subject,
                "wosid": faculty_page_attrs["wosid"],
                "3.10.7.5": "Search Courses"
            }
        )

    def get_courses_from_list_page(self, site_html):
        '''
            Returns a list of tuples containing the course info:
            (<subject/dept>, <4 digit code>, '<credit amount>', '<title>', '<current session link>')
        '''

        html_tag_format = \
            '<TR bgcolor="#[0-9A-Fa-f]+">[\n\t ]+<TD WIDTH=16%>[A-Z]+/([A-Z]+) +([0-9][0-9][0-9][0-9][a-zA-Z]?) +([0-9].[0-9][0-9])</TD>' + \
            '[\n\t ]+<TD WIDTH=24%> *([^\<\>]+) *</TD>' + \
            '[\n\t ]+<TD WIDTH=30%><a href="(/Apps/WebObjects/cdm.woa/\w+/\w+/\w+/[0-9.]+)">[^\<\>]+</a></TD>' + \
            '[\n\t ]+<TD WIDTH=30%></TD>[\n\t ]+</TR>'

        found_result = re.findall(html_tag_format, site_html)
        return found_result

    def get_desc_from_course(self, site_html):
        '''
        Returns the description of the course from the course page
        '''

        desc_tag_format = r'<[pP] class *= *"bold">Course Description:</[pP]>[\n\t ]*<[pP]>([^\<\>]+)</[pP]>'
        found_result = re.search(desc_tag_format, site_html)
        desc_scraped = found_result.group(1)
        return desc_scraped

    def get_prereq_from_desc(self, desc, current_course):
        '''
        Returns the prerequisites of the course from the description
        '''

        desc = desc.lower()

        start_ind = desc.find('prerequisite')
        stop_keywords = ['credit exclusion', 'not open to',
                         'may not be', 'may be taken', 'ncr', 'corequisite']
        stop_ind = len(desc)

        # we also want to stop at the first occurence of these stop keywords which signify a list of other contexts
        for keyword in stop_keywords:
            ind = desc.find(keyword)
            if ind < stop_ind and ind >= 0:
                stop_ind = ind

        # we want to find course codes in the paragraph, they will be of this format
        course_code_format = r'[a-z]*/*([a-z]+) *([0-9][0-9][0-9][0-9][a-zA-Z]?) +[0-9].[0-9]+'

        # extract parts where the prerequisite items are in
        desc_preqs = ''
        if start_ind >= 0 and stop_ind >= 0:
            desc_preqs = desc[start_ind:stop_ind]
        elif start_ind >= 0 and stop_ind < 0:
            desc_preqs = desc[start_ind:]
        else:
            return ''
        found_result = re.findall(course_code_format, desc_preqs)

        # a final safeguard: removing all entries that are higher (not equal) year level
        # to the current course, in case of 'Not open to: students who have taken GS/MGMT 4480'
        # also make sure it's not the exact same course, in case of 'PRIOR TO SUMMER: CSE 3212'
        # also make sure it's a course, not '[..]SUMMER 2014'
        level = int(current_course[1][0])
        pre_requirements = []

        for result in found_result:
            if int(result[1][0]) <= level and current_course[1] != result[1] and len(result[0]) >= 2:
                pre_requirements.append(result)

        # now we put the courses together as 1 string
        # concatenate each course into 1 str first i.e. ('eecs', '1012') -> 'eecs1012'
        prereqs = [requirements[0] + requirements[1]
                   for requirements in pre_requirements]

        return ' '.join(prereqs)

    def scrape_courses_from_dept(self, faculty_page_attrs, subject):
        '''
        Scrapes all courses from a department
        '''

        # get the page with the list of courses in the subject first
        list_page = self.get_list_page(faculty_page_attrs, subject)
        list_html = list_page.text

        # extract courses from the list page
        # this returns a list of tuples
        courses = self.get_courses_from_list_page(list_html)

        # loop through the list and read the description from the page
        courses_info = []
        for course in courses:
            # debug statement
            print(f"Current Scraping: {course[0]} {course[1]}")

            course_page_url = self.base_url + course[4]

            # request the page
            course_page = requests.get(course_page_url)

            # scrape the description from the page
            desc = self.get_desc_from_course(course_page.text)

            # scrape the prerequisites too
            prereqs = self.get_prereq_from_desc(desc, course)

            # now we can organize it into a dict
            res = {
                "dept": course[0].lower(),
                "code": course[1],
                "credit": float(course[2]),
                "name": course[3],
                "prereqs": prereqs,
                "desc": desc
            }
            courses_info.append(res)

        return courses_info

    def start_full_scrape(self):
        '''
        calling all the above functions together
        '''

        # for benchmarking
        start_time = time.time()

        # get the course search home site
        site = self.get_course_root_site()

        # from it extract the (current session) url to the 'by subject' site
        by_faculty_url = self.get_search_by_faculty_url(site)

        # request it to get the content
        by_faculty_page = requests.get(self.base_url + by_faculty_url).text

        # then get the important stuff from the page
        current_attributes = self.get_links_from_by_faculty_page(
            by_faculty_page)

        total_scraped = 0

        # in a loop, scrape all courses in each subject
        for subject in current_attributes["subjects"]:

            # hotfix to anti-ddos: create new session
            site = self.get_course_root_site()
            by_faculty_url = self.get_search_by_faculty_url(site)
            by_faculty_page = requests.get(self.base_url + by_faculty_url).text
            new_sess_attributes = self.get_links_from_by_faculty_page(
                by_faculty_page)

            # the subject's number in the current session's html form, and its 2-4 letter code
            subject_num = subject[0]
            subject_code = subject[1].lower()

            # for each subject, call the scrape function to get its courses
            subject_courses = self.scrape_courses_from_dept(
                new_sess_attributes, subject_num
            )
            num_courses = len(subject_courses)

            jobj = {"courses": subject_courses}

            # create file if it doesn't exist
            if not os.path.exists(self.export_dir):
                os.makedirs(self.export_dir)

            with open(os.path.join(self.export_dir, subject_code + ".json"), 'w', encoding="utf-8") as outfile:
                json.dump(jobj, outfile, indent=4)
            print(f"Scraped {num_courses} in dept {subject_code}")
            total_scraped += num_courses

        print(
            f"Scraped {total_scraped} in total, time taken: {(time.time() - start_time)}")


def main():
    '''
    TODO: Migrate to pytest
    '''
    course_scraper = CourseScraper(exportdir="../docs/data/courses")
    course_scraper.start_full_scrape()


if __name__ == '__main__':
    main()
