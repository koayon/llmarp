import random
import re

import requests
from bs4 import BeautifulSoup


def try_wiki_article():
    random_url = requests.get("https://en.wikipedia.org/wiki/Special:Random", timeout=5)
    soup = BeautifulSoup(random_url.content, "html.parser")
    soup_return = soup.find_all("p")
    num_paras = len(soup_return)
    random_para = soup_return[random.randint(0, num_paras - 1)]
    if soup_return:
        content = random_para.text
    else:
        raise ValueError("No content found")

    # print(len(content))
    if len(content) < 300:
        raise ValueError("Content too short")

    return content


def get_random_wiki_text():
    for _ in range(25):
        try:
            wiki_text = try_wiki_article()
            # Remove [number] citations with regex
            wiki_text = re.sub(r"\[\d+\]", "", wiki_text)
            return wiki_text
        except ValueError:
            continue


if __name__ == "__main__":
    print(get_random_wiki_text())
