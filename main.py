import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data

hdr = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.tor.com/series/malazan-reread-of-the-fallen/"

page = requests.get(url, headers=hdr)
soup = BeautifulSoup(page.text, 'html.parser')

skip_list = [13, 20, 34, 57, 84, 85, 86, 115, 116, 146, 175, 176, 205, 206, 242, 277, 290, 291, 322, 348, 349]

target_list = []
link_list = soup.find_all(class_='entry-header')
for i in link_list:
    content = i.contents[1]
    content = content.contents
    target = content[1]['href']
    target_list.append(target)
    #print(target)

collection = []
for i in range(0, 87):
    page = requests.get(target_list[i], headers=hdr)
    soup = BeautifulSoup(page.text, 'html.parser')

    lines = soup.find(class_="entry-content")
    n = str(lines).splitlines()
    strong_flag = 0


    for x in n:
        #edge cases (the website's fault...)
        if ("<p>CHAPTER EIGHT</p>") in x:
            strong_flag = 1
            collection.append("<p><strong>CHAPTER EIGHT</strong></p>")
            continue
        if ("<p><strong><span") in x: # Chapter 17 memories of ice, new reaction style..
            strong_flag = 0
            continue
        if ('<p><span style="text-decoration: underline"><strong>') in x: # Chapter 18 memories of ice, new reaction style..
            strong_flag = 0
            continue

        #real logic
        if ("<p><strong>" in x) and (len(x) < 100):  #found strong, either amanda or chapter summary or bill.
            if ("Amanda" in x) or ("Bill" in x) or ("commentary" in x): #Just commentary, skip this and all future
                strong_flag = 0
                continue
            strong_flag = 1 # not commentary, collect and all furture until next strong tag.
            collection.append(x)
            continue

        if (strong_flag == 1):
            collection.append(x)


#time to write it to html file
with open("malazan.html", "w") as file:
    for x in collection:
        print("_________________________________________________________________________")
        print(x)
        file.write(x)

#
# p = soup.find_all('p')
# for tag in p:
#     strongs = tag.find_all('strong')
#     for tag in strongs:
#         print(tag.text)
#         print(tag.find_next("p"))


#print(target_list)
#print(soup.prettify())

#night of knives chapter 5 is there twice, not my fault, chapter 5 should be chapter 6
