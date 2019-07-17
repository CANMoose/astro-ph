import astroph as aph
import sys
import smtplib

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
    send_email(body, n_matches)

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

if __name__ == '__main__':

    #ENTER YOUR KEYWORDS AND EMAIL HERE#
    keywords = ['IMF','initial mass function','mass function']
    email = 'meyer@astro.utoronto.ca'
    ####################################
    
    print "Sending astro-ph email..."

    create_email(keywords)
