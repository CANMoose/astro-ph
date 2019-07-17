import astroph as aph
import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(my_keywords, verbose=False):
    
    if verbose:
        print("Running astrophbot...\n")
        print("Checking arxiv...\n")
    
    artList = aph.get_artlist()
    
    if verbose:
        print("Arxiv downloaded, checking for the following keywords: ")
        for keyword in my_keywords:
            print(keyword + '\n')
    
    #Searching for keywords in abstracts
    kwdict = aph.find_in_abstracts(artList,my_keywords)
    
    #Starting email
    #ct=0
    body ="astroph-bot has searched the abstracts from today's astro-ph "+\
        "rss feed for the following keywords:"\
        +"\r\n"+",".join(my_keywords)+"\r\n\r\n"
    html ="<html></br><body></br>astroph-bot has searched the abstracts from today's astro-ph "+\
        "rss feed for the following keywords: "+", ".join(my_keywords)+"<br>"
    
    n_matches = 0
    #Building email
    for n,key in enumerate(kwdict.keys()):
            if len(kwdict[key]) > 0:
                #ct = ct + len(kwdict[key])
                body += "The following articles have the keyword: " + key + '\r\n'
                html += "<h3>The following articles have the keyword: " + key + '</h3>'
                
                body += "\r\n".join([artList[x].title + artList[x].link + '\r\n' + \
                        artList[x].abstract + '\r\n' for x in kwdict[key]]) + "\r\n\r\n"
                html += "<br>".join(['<b>'+artList[x].title+'</b>: '+ artList[x].link + '<br>' + \
                        artList[x].abstract + '<br>' for x in kwdict[key]]) + "<br><br>"
                n_matches += len(kwdict[key])
    
    if n_matches == 0:
        body += 'There were no matches to your keywords today...\r\n'
        html += 'There were no matches to your keywords today...<br>'

    if verbose:
        print("Sending email...\n")

    html += '</body></html>'
    
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    infofl = open('/home/pi/astrophinfo.txt','r')
    lines = infofl.readlines()

    sender = 'astroph.bot@gmail.com'
    pwd = lines[0][:-1]
    recipient = lines[1][:-1]

    message = MIMEMultipart("alternative")

    if n_matches == 0:
        message["Subject"] = 'astro-ph ALERT - NO MATCHES'
    else:
        message["Subject"] = 'astro-ph ALERT'

    #body = ""+body+""

    part1 = MIMEText(body, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, pwd)
        server.sendmail(sender, recipient, message.as_string())
        server.quit()
 
    #headers = ["From: " + sender,
    #       "Subject: " + subject,
    #       "To: " + recipient,
    #       "MIME-Version: 1.0",
    #       "Content-Type: text/plain"]

    #headers = "\r\n".join(headers)
    #session = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
 
    #session.ehlo()
    #session.starttls()
    #session.ehlo
    #session.login(sender, pwd)

    #session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)

    #session.quit()

    return

if __name__ == '__main__':

    #ENTER YOUR KEYWORDS AND EMAIL HERE#
    keywords = ['IMF','initial mass function','mass function']
    email = 'meyer@astro.utoronto.ca'
    ####################################
    
    print("Sending astro-ph email...")

    send_email(keywords)
