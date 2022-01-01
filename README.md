
# Yorku REST api *for all things York Univesity*
[![pytest](https://github.com/SSADC-at-york/Yoki/actions/workflows/pytest.yml/badge.svg)](https://github.com/SSADC-at-york/Yoki/actions/workflows/pytest.yml) [![pylint](https://github.com/SSADC-at-york/Yoki/actions/workflows/pylint.yml/badge.svg?branch=Aayush9029-patch-1)](https://github.com/SSADC-at-york/Yoki/actions/workflows/pylint.yml)

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
