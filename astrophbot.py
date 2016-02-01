import astroph as aph
import sys

def create_email(my_keywords,email,verbose=False):
    
    if verbose:
        print "Running astrophbot for %s\n" % (email)
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
    body ="astroph-bot has searched the abstracts from today's astro-ph "+\
        "rss feed for the following keywords:"\
        +"\r\n"+",".join(my_keywords)+"\r\n\r\n"
    
    no_cw = 0
    #Building email
    for n,key in enumerate(kwdict.keys()):
            if len(kwdict[key]) > 0:
                ct = ct + len(kwdict[key])
                body = body + "\r\n".join((["The following articles have "+\
                    "the keyword: "+key+"\r\n","\r\n".join([artList[x].title
                    + artList[x].link for x in kwdict[key]])])) + "\r\n\r\n"
                no_cw = 1 
    
    if not no_cw:
        body = body + 'There were no matches to your keywords today...\r\n'

    if verbose:
        print "Sending email to %s...\n" % (email)
    
    #send_email(str(sys.argv[1]),body)
    aph.send_email(email,body)

if __name__ == '__main__':

    #ENTER YOUR KEYWORDS AND EMAIL HERE#
    keywords = ['IMF','initial mass function','mass function']
    email = 'meyer@astro.utoronto.ca'
    ####################################
    
    print "Sending astro-ph email..."

    create_email(keywords,email)
