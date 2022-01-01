
# Yorku REST api *for all things York Univesity*
[![pytest](https://github.com/SSADC-at-york/Yoki/actions/workflows/pytest.yml/badge.svg)](https://github.com/SSADC-at-york/Yoki/actions/workflows/pytest.yml) [![pylint](https://github.com/SSADC-at-york/Yoki/actions/workflows/pylint.yml/badge.svg?branch=Aayush9029-patch-1)](https://github.com/SSADC-at-york/Yoki/actions/workflows/pylint.yml)

---

###  The problem 

I wanted a yorku API that I could use to automate tasks, navigate efficiently, find buildings, libraries cool hangout/study spots and so on.
#### And maybe create an app around it to help other students  ¯\\_(ツ)_/¯

---

### 💡 The solution 
Use Yorku official api, using endpoints they provide BUT THE ISSUE WAS  Yorku doesn't have an api, so I ended up creating my own.

---

### ✅ Who can use it?
Everyone. We welcome new contributions to our community.

---

### 💻 Endpoints 
- Food Building database, including open - close time.
- More to come... like courses, their ratings?, study spots, and so on.

---

### 🎉 Working JSON endpoints
[Yorku Dining Places Data](https://raw.githubusercontent.com/SSADC-at-york/Yoki/main/docs/data/dining.json)

_Example_
```json
  "data": [
    {
      "isOpen": false,
      "name": "Bakery @ Stong",
      "hours": null,
      "address": "Stong Dining Hall",
      "map_address": "Building 14"
    },
    {
      "isOpen": true,
      "name": "Bakery @ Winters",
      "hours": [
        "08:00",
        "21:00"
      ],
      "address": "Winters Dining Hall",
      "map_address": "Building 54"
    }
```
---

### Courses Data

```json
    "courses": [
        {
            "dept": "actg",
            "code": "2010",
            "credit": 3.0,
            "name": "Introduction To Financial Accounting I ",
            "prereqs": "",
            "desc": "This two core course sequence develops students' understanding of financial accounting information so that they can be informed and effective users of the information. The courses focus on uses of accounting information for different decisions and from different stakeholder perspectives, and consider the economic and behavioural effects that accounting treatments have on users and preparers. Readings from current publications are used to demonstrate practical applications of the issues discussed in class. Classroom techniques such as case studies, classroom discussions, student presentations and group and individual research projects (intended to develop students' critical skills) are employed.\r\n\r\nNote: SB/ACTG 2011 3.00 is not available to exchange students visiting Schulich unless it is a full year exchange and SB/ACTG 2010 3.00 is taken in the fall.\r\n\r\nCourse credit exclusions: GL/ECON 2710 3.00, AP/ECON 3580 3.00, AP/ECON 4200 3.00."
        },
        {
            "dept": "actg",
            "code": "2011",
            "credit": 3.0,
            "name": "Introduction To Financial Actg II",
            "prereqs": "",
            "desc": "This two-course sequence develops students' understanding of financial accounting information so that they can be informed and effective users of the information. The courses focus on uses of accounting information for different decisions and from different stakeholder perspectives, and consider the economic and behavioural effects that accounting treatments have on users and preparers. Readings from current publications are used to demonstrate practical applications of the issues discussed in class. Classroom techniques such as case studies, classroom discussions, student presentations and group and individual research projects (intended to develop students' critical skills) are employed.\r\nPrerequisite: SB/ ACTG 2010 3.00.\r\nCourse Credit Exclusion: GL/ECON 2710 3.00."
        },
```

####  ⚠️ NOTE:  DO NOT RUN course_scraper.py a lot it sends a lot of multithreaded request
Use the pre-cached jsons files that's in [docs/data/courses](https://github.com/SSADC-at-york/Yoki/tree/main/docs/data/courses)

> pls offload :), it's faster to fetch from github anyways!

---

### 🙏 Thank you

- [@PresidentKevvol](https://github.com/PresidentKevvol)

