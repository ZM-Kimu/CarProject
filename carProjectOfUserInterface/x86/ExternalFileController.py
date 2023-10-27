import os
import datetime


class Log:

    def __init__(self) -> None:
        self.LogFile = "MainUILog.txt"
        self.__ReadLog()

    def __ReadLog(self):
        Dir, = "None",
        for A, _, C in os.walk(os.getcwd()):
            if self.LogFile in C:
                Dir = A
                break
        if os.path.exists(Dir+"/"+self.LogFile):
            self.LogOpen = open(Dir+"/"+self.LogFile, "rt+",encoding="UTF-8")
        else:
            self.LogOpen = open(os.getcwd()+"/"+self.LogFile, "wt+",encoding="UTF-8")

    # Status 0 means Exit Normally, 1 means Restart
    def MainInitalize(self):
        self.LogOpen.seek(0, 0)
        Read = self.LogOpen.readline().strip("\n")
        if "Status" in Read and "Port" in Read:
            Status = eval(Read)
        else:
            Status = self.ChangeInitalizeStatus()
        return Status

    def ChangeInitalizeStatus(self, Status=0, Port="COM5", BandRate=115200, Music=0, MusicTime=0, Path=""):
        self.LogOpen.seek(0, 0)
        self.LogOpen.write(
            "{"+f'"Status":"{Status}","Port":"{Port}","BandRate":"{BandRate}","MusicNow":"{Music}","MusicPosition":"{MusicTime}","MusicPath":"{Path}"'+"}\n")
        return {"Status": Status, "Port": Port, "MusicNow": Music, "MusicPosition": MusicTime, "MusicPath": Path}

    def BuildLog(self, Title, Text):
        Time = datetime.datetime.now()
        self.LogOpen.seek(0, 2)
        self.LogOpen.write(str(Time)+"\n"+str(Title)+"\n"+str(Text)+"\n")

    def Close(self):
        self.LogOpen.close()


class Config:

    def __init__(self) -> None:
        self.ConfigFile = "main.cfg"
        self.__ReadConfig()
        self.ApplyConfig()

    def __ReadConfig(self):
        Dir = "None"
        for A, _, C in os.walk(os.getcwd()):
            if self.ConfigFile in C:
                Dir = A
                break
        if os.path.exists(Dir+"/"+self.ConfigFile):
            self.ConfigOpen = open(Dir+"/"+self.ConfigFile, "rt+",encoding="UTF-8")
        else:
            self.ConfigOpen = open(os.getcwd()+"/"+self.ConfigFile, "wt+",encoding="UTF-8")
            self.WriteTemplate()
        self.FormatConfig()

    def FormatConfig(self):
        read="a"
        attribution="First"
        self.options={}
        attributions={}       
        while read!="":
            read=self.ConfigOpen.readline()
            if read == "\n":
                continue
            read=read.strip("\n")
            if "#" in read and read[0] == "#":
                continue
            elif "[" in read and "]" in read:
                self.options[attribution]=attributions
                attribution=read[1:-1]
                attributions={}
            elif "=" in read:
                equalIndex=read.index("=")
                attributions[read[:equalIndex]] = read[equalIndex+1:]
            if read == "":
                self.options[attribution]=attributions
        del self.options["First"]
        return self.options

    def ApplyConfig(self):

        def Format(judgement):
            if judgement == "True" or judgement == "true":
                return True
            elif judgement == "False" or judgement == "false":
                return False
            else:
                return judgement
        if "Appearance" in self.options:
            attribution = self.options["Appearance"]
            if "FullScreen" in attribution:
                self.isFullScreen = Format(attribution["FullScreen"])
            if "Language" in attribution:
                self.language = Format(attribution["Language"])
            if "Animation" in attribution:
                self.animationOn = Format(attribution["Animation"])

        if "Experimental" in self.options:
            attribution = self.options["Experimental"]
            if "StopBackgroundCircles" in attribution:
                self.OffCircles = Format(attribution["StopBackgroundCircles"])

        self.ConfigOpen.close()

    def WriteTemplate(self):
        text = """#This is the config file of MainUI

[Appearance]
#Define whether the main screen is full screen.
FullScreen=False
#This option use to set the language of UI.
Language=chinese
#Set the global animation is on or off.
Animation=False
#

[Operation]

[Visual]

[External]

This part is experimental, you can config it you want.
[Experimental]
#If you feeling slowly, may be caused by background circles, turn it on.
StopBackgroundCircles=True
"""
        self.ConfigOpen.write(text)

class Language:

    def __init__(self,language) -> None:
        self.languagePack="language.pak"
        self.ConfigLanguage=language
        result=self.__GetConfigFile()
        self.Result=result
        if self.Result != None:
            self.ReadPack()
            self.ReturnText()

    def __GetConfigFile(self):
        Dir = "None"
        for A, _, C in os.walk(os.getcwd()):
            if self.languagePack in C:
                Dir = A
                break
        if os.path.exists(Dir+"/"+self.languagePack):
            self.languageOpen = open(Dir+"/"+self.languagePack, "rt+",encoding="UTF-8")
            return self.languageOpen
        else:
            return None

    def ReadPack(self):
        isFirst=True
        sequencyNum=-1
        read="a"
        mappingSet=[]                
        self.languagesDict={}
        self.allMapping={}
        while read!="":
            read=self.languageOpen.readline()
            if read == "\n":
                continue
            read=read.strip("\n")
            if isFirst and "[" in read and "]" in read:
                languages=read[1:-1].split(",")
                for language in languages:
                    self.languagesDict[int(language[0])]=language[2:]
                isFirst=False
            elif "$" in read and read[0] == "$":
                attributionNow=read[1:]
                sequencyNum=len(languages)
            else:
                mappingSet.append(read)
                sequencyNum -= 1
            if sequencyNum==0:
                self.allMapping[attributionNow]=mappingSet
                mappingSet=[]       

    def ReturnText(self):
        mappingDict={}
        for num,lan in self.languagesDict.items():
            if self.ConfigLanguage.lower() in lan:
                for var,string in self.allMapping.items():
                    mappingDict[var]=string[num-1]
                break
        self.lang=mappingDict
        

