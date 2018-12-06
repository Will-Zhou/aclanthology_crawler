import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import requests
import time
import os
import re


def getFile(url, file_name):
    retry = 0
    flag = False
    while retry < 3:
        try:
            u = urllib.request.urlopen(url)
            flag = True
        except urllib.error.HTTPError:
            print(url, "url file not found")
            retry += 1
        if flag:
            block_sz = 8192
            f = open(file_name, 'wb')
            buffer = u.read(block_sz)
            while buffer:
                f.write(buffer)
                buffer = u.read(block_sz)
            print("Sucessful to download" + " " + url)
            f.close()
            retry = 3
        time.sleep(5)


def get_web(url):
    html = ""
    reTry = 0
    while True and reTry < 3:
        try:
            html = requests.get(url).text
            break
        except:
            reTry += 1
    time.sleep(3)
    return html


if __name__ == "__main__":
    root = "https://aclanthology.info"
    web_list = ["https://aclanthology.info/venues/acl", "https://aclanthology.info/venues/eacl",
                "https://aclanthology.info/venues/naacl", "https://aclanthology.info/venues/semeval",
                "https://aclanthology.info/venues/emnlp", "https://aclanthology.info/venues/conll",
                "https://aclanthology.info/venues/ws", "https://aclanthology.info/venues/cl"]
    # web_list = web_list[0:1]
    for web in web_list:
        html = get_web(web)
        soup = BeautifulSoup(html, 'html.parser')
        events = soup.find_all("h4")

        meetings = []
        for e in events:
            link = e.next.get("href")
            meetings.append(root + link)
            year = int(e.next.text.split(" ")[1])
            if year < 2000:
                break

        for m in meetings:
            tdir = m.split("/")
            tdir = tdir[len(tdir)-1]
            if not os.path.exists(tdir):
                os.mkdir(tdir)
            fw = open(tdir + "/bibs.txt", mode="a", encoding="utf-8")
            meeting_html = get_web(m)
            meeting_soup = BeautifulSoup(meeting_html, "html.parser")
            papers = meeting_soup.find_all("p")
            for paper in papers:
                details = paper.find_all("a")
                # get pdf
                pdf_url = details[0].get("href")
                title = pdf_url.split("/")
                title = tdir + "/" + title[len(title)-1] + ".pdf"

                if not os.path.exists(title):
                    if re.findall("[a-zA-z]+://[^\s]*", pdf_url):
                        getFile(pdf_url, title)
                        # get bib
                        bib_url = root+details[1].get("href")
                        bib = get_web(bib_url)
                        fw.write(bib + "\n")
            fw.close()

    print("The End.")
