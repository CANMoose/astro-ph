import urllib
import xml.etree.ElementTree as ET
import re
import smtplib
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
def print_titles(art_list,group='all'):
    '''Possible groups are astro-ph.GA, astro-ph.SR, astro-ph.IM, astro-ph.CO, 
    astro-ph.HE, astro-ph.HE'''

    if group == 'all':
        for n, art in enumerate(art_list):
            print str(n) + ':' + art.title + '\n'
    else:
        for n, art in enumerate(art_list):
            if art.group == 'astro-ph.'+group:
                print str(n) + ':   ' + art.title + '\n'
    
    return

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


def send_email(body, n_matches):

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    infofl = open('/home/pi/astrophinfo.txt','r')
    lines = infofl.readlines()

    sender = 'astroph.bot@gmail.com'
    pwd = lines[0][:-1]
    recipient = lines[1][:-1]

    if n_matches == 0:
        subject = 'astro-ph ALERT - NO MATCHES'
    else:
        subject = 'astro-ph ALERT'


    body = ""+body+""
 
    headers = ["From: " + sender,
           "Subject: " + subject,
           "To: " + recipient,
           "MIME-Version: 1.0",
           "Content-Type: text/plain"]

    headers = "\r\n".join(headers)
    session = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
 
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, pwd)

    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)

    session.quit()

    return

################################################
if __name__ == '__main__':

    artList = get_artlist()
    my_keywords = ['IMF','Initial Mass Function', 'Mass Function']

    test=find_in_abstracts(artList,my_keywords)

    ct=0
    body ="astroph-bot has searched the abstracts from today's astro-ph rss "+\
        +"feed for the following keywords:"+"\r\n"+",".join(my_keywords)+\
        "\r\n\r\n"

    for n,key in enumerate(test.keys()):
            if len(test[key]) > 0:
                ct = ct + len(test[key])
                body = body + "\r\n".join((["The following articles have the"+\
                    " keyword: "+key+"\r\n","\r\n".join([artList[x].title + \
                    artList[x].link for x in test[key]])])) + "\r\n\r\n"

    if ct > 0: 
        #send_email(str(sys.argv[1]),body)
        send_email('meyer@astro.utoronto.ca',body)





