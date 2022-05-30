import json
import os
import re

all_data = []


def seperate_string_num(string):
    # add space between dept and code
    # example
    #  hreq1010 -> hreq 1010
    string = re.sub(r'([a-zA-Z]{3})([0-9]{3})', r'\1 \2', string)
    # constant case for name CAPITAL
    name = string.split(' ')[0]
    name = name.upper()
    code = string.split(' ')[-1].lower()
    if name == code:
        return name
    return name + ' ' + code


def clean_text(string):
    # make sure str is a string
    string = str(string)
    string = string.strip()
    # remove all unicode characters
    string = string.encode('ascii', 'ignore').decode('ascii')

    string = string.strip()
    string = string.replace('\n', ' ')
    string = string.replace('\r', ' ')
    string = string.replace('\t', ' ')
    string = string.replace('  ', ' ')

    return string


# go through all .json files in courses raw json folder
for file in os.listdir("courses_raw_json"):
    departments = []
    # deparments is a list dict in the file

    if file.endswith(".json"):
        # open file and read it
        with open("courses_raw_json/" + file) as json_file:
            file_data = json.load(json_file)
            '''
            example of file_data: structure of a single json file
            {
                "dept": "actg",
                "code": "2010",
                "credit": 3.0,
                "name": "Introduction To Financial Accounting I ",
                "prereqs": "",
                "desc": "This two core course sequence develops students' understanding of financial accounting information so that they can be informed and effective users of the information. The courses focus on uses of accounting information for different decisions and from different stakeholder perspectives, and consider the economic and behavioural effects that accounting treatments have on users and preparers. Readings from current publications are used to demonstrate practical applications of the issues discussed in class. Classroom techniques such as case studies, classroom discussions, student presentations and group and individual research projects (intended to develop students' critical skills) are employed.\r\n\r\nNote: SB/ACTG 2011 3.00 is not available to exchange students visiting Schulich unless it is a full year exchange and SB/ACTG 2010 3.00 is taken in the fall.\r\n\r\nCourse credit exclusions: GL/ECON 2710 3.00, AP/ECON 3580 3.00, AP/ECON 4200 3.00."
            },

            appended to data format:
            [
                "dept": "actg",
                {
                    "code": "2010",
                    "credit": 3.0,
                    "name": "Introduction To Financial Accounting I ",
                    "prereqs": "",
                    "desc": ""
                    },
                {...}
                ]
            '''
            for course in file_data["courses"]:
                code = clean_text(course["code"])
                name = clean_text(course["name"])
                credit = clean_text(course["credit"])
                prereqs = clean_text(course["prereqs"])
                desc = clean_text(course["desc"])

                if code == "" or name == "":
                    continue

                if prereqs == "":
                    prereqs = []
                else:
                    prereqs = prereqs.replace("  ", " ")
                    prereqs = prereqs.replace("\r\n", " ")
                    prereqs = prereqs.split()

                new_prereqs = []
                for prereq in prereqs:
                    clean_pre = seperate_string_num(prereq)
                    if clean_pre not in new_prereqs:
                        new_prereqs.append(clean_pre)

                if desc == "N/A" or desc == "":
                    desc = "No Description Provided"
                else:
                    desc = desc.replace("\r\n", " ")
                    desc = desc.replace("\n", " ")
                    desc = desc.replace("\t", " ")
                    desc = desc.replace("  ", " ")
                    desc = desc.replace("   ", " ")
                course = {
                    "code": code,
                    "name": name,
                    "credit": credit,
                    "prereqs": new_prereqs,
                    "desc": desc
                }
                if course not in departments:
                    departments.append(
                        course
                    )
            if len(file_data["courses"]) == 0:
                continue
            if len(departments) == 0:
                continue
    # sort departments by code
    departments.sort(key=lambda x: x["code"])
    all_data.append(
        {
            "dept": file_data["courses"][0]["dept"].upper(),
            "courses": departments
        }
    )

# sort all_data by dept
all_data.sort(key=lambda x: x["dept"])

# write all_data to courses.json
with open("courses.json", "w") as outfile:
    json.dump(all_data, outfile, indent=4)
