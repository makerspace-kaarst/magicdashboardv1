#!/usr/bin/env python3

import pygame,random
import sys
import Wetter
import JCscraper as jcs
Change = 100000
basepath="/home/pi/Content/"
File = open(basepath+"Init/Config.txt","r")
Lines = File.readlines()
File.close()
for Line in Lines :
    if "Vollbild" in Line :
        var = Line.split(" ")[2]
        if var.rstrip() == "True":
            print("Test")
            screen = pygame.display.set_mode([1280,800],pygame.FULLSCREEN)
        else :
            screen = pygame.display.set_mode([1280,800])
    if "Speed" in Line :
        Speed = int(Line.split(" ")[2].rstrip())
        Change = Speed + 100
    if "WetterLink" in Line :
        Region = Line.split(" = ")[1]
def Update() :
    File = open(basepath+"Init/Config.txt","r")
    Lines = File.readlines()
    File.close()
    for Line in Lines :
        if "Vollbild" in Line :
            var = Line.split(" ")[2]
            if var.rstrip() == "True":
                screen = pygame.display.set_mode([1280,800],pygame.FULLSCREEN)
            else :
                screen = pygame.display.set_mode([1280,800])
        if "Speed" in Line :
            Speed = int(Line.split(" ")[2].rstrip())
            Change = Speed + 100
        if "WetterLink" in Line :
            Region = Line.split(" = ")[1]
    return Speed,screen,Region
def Update_Userdata ():
    Userdata = open(basepath+"User/Userdata.txt","r")
    Userdata2 = Userdata.readlines()
    Userdata.close()
    return Userdata2
class Filehandle () :
    def __init__ (self,File):
        self.name = File
        self.File = open(File,"r")
        self.Lines = self.File.readlines()
        self.Backup = self.Lines[:]
        self.File.close()
    def Update(self):
        if self.Lines == [] :
            self.File = open(self.name,"r")
            self.Lines = self.File.readlines()
            self.Backup = self.Lines[:]
            self.Lines = self.Backup
            self.File.close()
        Out = self.Lines[0]
        self.Lines.remove(Out)
        if "<img>" in Out :
            Out = list(Out)[5:]
            Out2 = Out
            Out = ""
            for Item in Out2 :
                Out += Item
            PNG = pygame.image.load(basepath+"Bild/"+Out.rstrip())
            return "Img",PNG
        if "<Wetter>" in Out :
            return "Wetter",None
        if "<br>" in Out :
            return "Br","Fail"
        if "<JC>" in Out:
            return "JC",None
        else :
            return "Text",Out.rstrip()
pygame.init()
pygame.mouse.set_visible(False)
Aktiv = True
f1_font = pygame.font.Font(None, 50)
pygame.display.flip()
Fileh = Filehandle(basepath+"Init/Input_Text.txt")
Pos = 20
YPos = 20
Update_Stats =5
#Daten der gesichtserkennung und anderer Externer Systeme
Userdata = Update_Userdata()
User_name = Userdata[0].rstrip()
User_alter = Userdata[1].rstrip()
User_anrede = Userdata[2].rstrip()
User_titel = Userdata[3].rstrip()
Uhr = pygame.time.Clock()
Speed,screen,Region = Update()
while Aktiv :
    Uhr.tick(10)
    Change +=0.1
    if Change >= Speed :
        #try:
        if True:
            Speed,screen,Region = Update()
            Update_Stats += 1
            Type,Text = Fileh.Update()
            Userdata = Update_Userdata()
            User_name = Userdata[0].rstrip()
            User_alter = Userdata[1].rstrip()
            User_anrede = Userdata[2].rstrip()
            User_titel = Userdata[3].rstrip()
            TextData = []
            if Type == "Text" :
                Text_Data = open(basepath+"Text/"+Text+".txt","r")
                Text_Data2 = Text_Data.readlines()
                try :
                    Pos_data = Text_Data2[0].split(" : ")
                    Pos = int(Pos_data[0].rstrip())
                    YPos = int(Pos_dat[1].rstrip())
                    Text_Data1 = Text_Data1[1:]
                    Text_Data2 = Text_Data2[1:]
                    Text_Data3 = Text_Data3[1:]
                    TextDatafailsave = [Text_Data1, Text_Data2, Text_Data3]
                except :
                    Pos = 20
                    YPos = 20
                Text_Data.close()
                Text_List = []
                for ID,Item in enumerate(Text_Data2) :
                    Item = Item.replace("@name",User_name)
                    Item = Item.replace("@alter",User_alter)
                    Item = Item.replace("@titel",User_titel)
                    Item = Item.replace("@anrede",User_anrede)
                    f1_surf = f1_font.render(Item.rstrip(), 50 , (255,255,255))
                    Text_List.append(f1_surf)
            elif Type == "Img" :
                Text_List = []
                Text_List.append(Text)
            elif Type == "JC":
                Text_List_Raw = jcs.get()
                Text_List = []
                for t in Text_List_Raw:
                    Text_List.append(f1_font.render(t, 20 , (255,255,255)))
            elif Type == "Wetter":
                Text_List = []
                Wetterdata = Wetter.Get(Region)

                for iid,Item in enumerate(Wetterdata) :
                    if iid == 0:
                        f1_surf = f1_font.render(Item, 20 , (255,125,0))
                    else:
                        f1_surf = f1_font.render(Item, 20 , (255,255,255))
                    Text_List.append(f1_surf)
            elif Type == "Br" :
                Change = 0
            screen.fill([0,0,0])
            if Change != 0 :
                for ID,Item in enumerate(Text_List):
                    screen.blit(Item, [Pos,ID*40 +YPos])
                    pygame.display.flip()
            Change = 0
            pygame.display.flip()
        #except:
        else:
            screen.fill([255,0,0])
            Update_Stats += 1
            pygame.display.flip()
    for event in pygame.event.get() :

        if event.type == pygame.QUIT :
            Aktiv = False
        elif event.type == pygame.KEYDOWN :
            Aktiv = False
pygame.quit()
