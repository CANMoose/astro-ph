import astroph as aph
import sched, time

def create_email(keywords,email):

    artList = aph.get_artlist()
    kwdict = aph.find_in_abstracts(artList,my_keywords)

    ct=0
    body ="astroph-bot has searched the abstracts from today's astro-ph rss feed for the following keywords:"\
        +"\r\n"+",".join(my_keywords)+"\r\n\r\n"
    for n,key in enumerate(kwdict.keys()):
            if len(test[key]) > 0:
                ct = ct + len(kwdict[key])
                body = body + "\r\n".join((["The following articles have the keyword: "\
                    +key+"\r\n","\r\n".join([artList[x].title + artList[x].link for x in kwdict[key]])]))\
                    + "\r\n\r\n"
    
    if ct > 0: 
        #send_email(str(sys.argv[1]),body)
        aph.send_email(email,body)


if __name__ == '__main__':
    s = sched.schedular(time.time, time.sleep)

    keywords = ['IMF','Initial Mass Function', 'Mass Function']
    email = 'meyer@astro.utoronto.ca'

    nsec_day = 86400

    s.enter(60,1, create_email(keywords,email))


