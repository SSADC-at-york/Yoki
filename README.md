
# YorkU REST API — for all things York University
[![pytest](https://github.com/SSADC-at-york/Yoki/actions/workflows/pytest.yml/badge.svg)](https://github.com/SSADC-at-york/Yoki/actions/workflows/pytest.yml) [![pylint](https://github.com/SSADC-at-york/Yoki/actions/workflows/pylint.yml/badge.svg?branch=Aayush9029-patch-1)](https://github.com/SSADC-at-york/Yoki/actions/workflows/pylint.yml)

---

### The problem 

I wanted a YorkU API that I could use to automate tasks and navigate efficiently. I also wanted to find buildings, libraries, cool hangout / study spots, and so on. And maybe create an app around it to help other students ¯\\_(ツ)_/¯

---

### 💡 A solution

It'd be nice to use an official YorkU API, using endpoints they provide. But YorkU doesn't have an API, so I ended up creating my own.

---

### ✅ Who can use it?

Everyone. We welcome new contributions to our community.

---

### 💻 Endpoints 

- Dining places database, including and close times.
- Courses data, including course descriptions and more (but not schedules).

(Ideas for future endpoints: course ratings, study spots, et cetera.)

---

### 🎉 Working JSON endpoints

[YorkU dining places data](https://raw.githubusercontent.com/SSADC-at-york/Yoki/refs/heads/main/docs/data/dining/dining.json)

_Example:_
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

[YorkU courses data](https://github.com/SSADC-at-york/Yoki/tree/main/docs/data/courses)

_Example:_
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

#### ⚠️ Note: Do not run course_scraper.py a lot. It sends a lot of multithreaded requests.

Use the pre-cached json files found in [docs/data/courses](https://github.com/SSADC-at-york/Yoki/tree/main/docs/data/courses)

Pls offload :), it's faster to fetch from GitHub anyway!

---

### 🙏 Thank you

- [@PresidentKevvol](https://github.com/PresidentKevvol)

---

### Other York University APIs

Some other York University APIs, made by other students, include:

*  https://github.com/Aayush9029/YorkuPublic/branches/all
*  https://yorkapi.isaackogan.com/ by [@isaackogan](https://github.com/isaackogan) — [(source)](https://github.com/isaackogan/YorkUAPI)
*  https://github.com/A-Chidalu/YU-Developer-API
*  https://github.com/jackehuynh/EasyYU-API
*  https://github.com/mlisbit/openYorkU-API
