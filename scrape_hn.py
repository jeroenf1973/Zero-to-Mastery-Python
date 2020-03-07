import pprint

import requests
from bs4 import BeautifulSoup

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
links = (soup.select('.storylink'))
subtext = (soup.select('.subtext'))


def sort_story_by_votes(hn_list):
    """ return sorted(hn_list), maak gebruik van éénmalig 
    lambda functie om te sorteren op aantal votes
    """
    return sorted(hn_list, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    """ een list met artikelen van hackernews pagina met meer dan 100 votes
    """
    hn = []
    for index, item in enumerate(links):
        # enumarte geeft teller/index mee in list
        title = links[index].getText()
        # default waarde voor als er geen link is
        href = links[index].get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_story_by_votes(hn)


pprint.pprint(create_custom_hn(links, subtext))
