from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
def Get(Link):
    data = urlopen(Link).read()
    soup = BeautifulSoup(data,"html.parser")
    element = soup.find('table', attrs={'class': "weather-overview desk-mb+ portable-mb"})
    PT = soup.get_text()
    Junk = PT.split("Morgens")[0]
    PT = PT.split("Morgens")[1]
    PT = PT.replace(" ","")
    PT = PT.strip()
    PT = PT.split("<")[0]
    PT = PT.replace("\n\n","\n")
    PT = PT.split("\n")
    WD = []
    #SplitData
    Wolken = []
    Temp = []
    for Item in PT:
        if Item not in [""," ","\n"]:
            WD.append(Item)
    Junk = Junk.split("?")[-1]
    Junk = Junk.split(".")[-1]
    Junk = Junk.split("\n")
    DayTimeName = []
    for Line in Junk:
        if Line != "":
            Data = Line.strip()
            if Data != "":
                DayTimeName.append(Data)
    for ID,Content in enumerate(WD):
        if ID in [0,1,2,3]: Temp.append(Content)
        if ID in [4,5,6,7]: Wolken.append(Content)
    Proz = re.findall("\d.\u202f%"," ".join(WD))
    NProz = []
    for Line in Proz:
        NProz.append(Line.replace("\u202f%",""))
    Regenw = NProz[:4]
    Feuchte = NProz[4:]
    #Seperate Data into Daytime
    FinalText = []
    Mittags = [DayTimeName[0]+":"]
    Abends = [DayTimeName[1]+":"]
    Nachts = [DayTimeName[2]+":"]
    Morgens = ["Morgen:"]
    Data = ["Zeit","Temp","Regen(%)","Wolken(%)","Feuchte"]
    for ID,Use in enumerate([Temp,Regenw,Wolken,Feuchte]):
        while len(Use) <= 4:
            Use.append("?")
        if ID in [1,3]:
            for ID,Item in enumerate(Use):
                Item +="%"
                Use[ID] = Item
        Mittags.append(Use[0])
        Abends.append(Use[1])
        Nachts.append(Use[2])
        Morgens.append(Use[3])
    FinalText.append("%12s %12s %12s %17s %8s"%tuple(Data))
    FinalText.append("%12s %12s %12s %17s %8s"%tuple(Mittags))
    FinalText.append("%12s %12s %12s %17s %8s"%tuple(Abends))
    FinalText.append("%12s %12s %12s %17s %8s"%tuple(Nachts))
    FinalText.append("%12s %12s %12s %17s %8s"%tuple(Morgens))
    return FinalText
