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

    return content, random_url.url


def get_random_wiki_text():
    for _ in range(25):
        try:
            wiki_text, wiki_url = try_wiki_article()
            # Remove [number] citations with regex
            wiki_text = re.sub(r"\[\d+\]", "", wiki_text)
            return wiki_text, wiki_url
        except ValueError:
            continue


BACKUP_SENTENCE = """Later in the same 1960 publication Solomonoff describes his extension of the single-shortest-code theory. This is Algorithmic Probability. He states: "It would seem that if there are several different methods of describing a sequence, each of these methods should be given some weight in determining the probability of that sequence." He then shows how this idea can be used to generate the universal a priori probability distribution and how it enables the use of Bayes rule in inductive inference. Inductive inference, by adding up the predictions of all models describing a particular sequence, using suitable weights based on the lengths of those models, gets the probability distribution for the extension of that sequence. This method of prediction has since become known as Solomonoff induction."""


if __name__ == "__main__":
    print(get_random_wiki_text())
