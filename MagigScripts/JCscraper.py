from bs4 import BeautifulSoup
import urllib3
import random
def get():
    file = open("/home/pi/nas/Content/Init/JC_Website_Reference.txt","r")
    websites = file.readlines()
    file.close()
    url =random.choice(websites).rstrip()
    print(url)
    http_pool = urllib3.connection_from_url(url)
    html = http_pool.urlopen('GET',url).data
    soup = BeautifulSoup(html,features="html.parser")
    rows = soup.findAll('p')
    output = []
    for d in rows[1:]:
        text = d.text.split("</span>")[0]
        if text not in [""," ","\n"]:
            prox = text.split(" ")
            count = 0
            lineCount = 0
            line = ""
            for word in prox:
                if count < 55:
                    count += len(word)+1
                    line += word + " "
                else:
                    lineCount += 1
                    output.append(line)
                    count = 0
                    line = ""
            if line != "":
                output.append(line)
                

    heading = output[0]
    return output
