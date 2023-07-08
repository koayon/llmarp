import webbrowser

import requests
from bs4 import BeautifulSoup

random_url = requests.get("https://en.wikipedia.org/wiki/Special:Random", timeout=5)
soup = BeautifulSoup(random_url.content, "html.parser")
soup_return = soup.find(class_="firstHeading")
if soup_return:
    title = soup_return.title
else:
    raise ValueError("No title found")

page_url = "https://en.wikipedia.org/wiki/%s" % title
print(page_url)

soup = BeautifulSoup(random_url.content, "html.parser")
soup_return = soup.find("p")
print(soup_return)
