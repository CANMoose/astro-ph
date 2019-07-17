import urllib
import xml.etree.ElementTree as ET
import re
import sys

class Article(object):
    '''Produces an article object so you can easily access an article's title, abstract
    authros, regular link, and pdf link'''

    def __init__(self, title,link,abstract,authors):

        new_title = re.sub('\(([^)]*)\)','', title)
        self.title = new_title

        self.link = link
        
        abstract = re.sub('<[^>]*>','',abstract)
        abstract = abstract.replace('\n', ' ')
        abstract = abstract.strip()
        self.abstract = abstract

        authors = re.sub('<[^>]*>','',authors)
        authors = authors.strip()
        self.authors = authors

        title_cut = re.findall('\[([^]]*)\]', title)
        if len(title_cut) == 0:
            self.group = re.findall('\(([^]]*)\)',title)[0]
        else:
            self.group = title_cut[0]
        
        linkspl = link.split('/')
        self.pdflink = 'http://arxiv.org/pdf/' + linkspl[-1]

def get_artlist():
    '''Produces a list of article objects from the most recent (i.e. today's) astro-ph 
    postings.'''

    url = 'http://export.arxiv.org/rss/astro-ph'

    data = urllib.urlopen(url).read()
    root = ET.fromstring(data)

    artList = []

    for n,item in enumerate(root):
        if n > 1:
            artList.append(Article(item[0].text,item[1].text,item[2].text,item[3].text))

    return artList
    
######################################################
# Tools

def find_in_abstracts(artList, s):
    '''Finds keywords in the list of strings s in the abstracts. Returns a 
    dictionary matching the keywords and the matched article number'''

    matched_articles = {}
    for keyword in s: matched_articles[keyword] = []
    for n,art in enumerate(artList):
        for keyword in s:
            if keyword.lower() in art.abstract.lower() and n not in matched_articles[keyword]:
                matched_articles[keyword].append(n)

    return matched_articles

################################################
if __name__ == '__main__':

    pass




