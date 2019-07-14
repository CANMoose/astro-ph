import astroph as aph
import sys

def create_email(my_keywords,verbose=False):
    
    if verbose:
        print "Running astrophbot...\n"
        print "Checking arxiv...\n"
    
    artList = aph.get_artlist()
    
    if verbose:
        print "Arxiv downloaded, checking for the following keywords: "
        for keyword in my_keywords:
            print keyword
            print '\n'
    
    #Searching for keywords in abstracts
    kwdict = aph.find_in_abstracts(artList,my_keywords)
    
    #Starting email
    ct=0
    body ="<html><body>astroph-bot has searched the abstracts from today's astro-ph "+\
        "rss feed for the following keywords:"\
        +"\r\n"+",".join(my_keywords)+"\r\n\r\n"
    
    no_cw = 0
    n_matches = 0
    #Building email
    for n,key in enumerate(kwdict.keys()):
            if len(kwdict[key]) > 0:
                ct = ct + len(kwdict[key])
                body = body + "\r\n".join((["<b>The following articles have "+\
                    "the keyword: "+key+"</b>\r\n","\r\n".join([artList[x].title
                    + artList[x].link + '\r\n' + artList[x].abstract + '\r\n' for x in kwdict[key]])])) + "\r\n\r\n"
                no_cw = 1 
                n_matches += len(kwdict[key])
    
    if not no_cw:
        body = body + 'There were no matches to your keywords today...\r\n'

    if verbose:
        print "Sending email...\n"

    body += '</body></html>'
    
    #send_email(str(sys.argv[1]),body)
    aph.send_email(body, n_matches)

if __name__ == '__main__':

    #ENTER YOUR KEYWORDS AND EMAIL HERE#
    keywords = ['IMF','initial mass function','mass function']
    email = 'meyer@astro.utoronto.ca'
    ####################################
    
    print "Sending astro-ph email..."

    create_email(keywords)
