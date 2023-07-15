import os
from pygame import mixer


class Music:

    def __init__(self):
        self.MusicNow = 0
        self.Total = 0
        self.FolderPath = ""
        self.MusicList = []
        mixer.init()

    def GetFiles(self, FolderPath):
        self.__init__()
        self.FolderPath = FolderPath
        for _, _, Files in os.walk(FolderPath):
            for File in Files:
                if File.endswith(".wav") or File.endswith(".mp3"):
                    self.MusicList.append(File)
        self.Total = len(self.MusicList)

    def LoadAndPlay(self, MusicNow=0, Time=0, Folder=".", IsRestart=False):
        try:
            if IsRestart:
                self.MusicNow = MusicNow
                self.GetFiles(Folder)
            mixer.music.load(self.FolderPath+"/"+self.MusicList[self.MusicNow])
            mixer.music.play(start=Time)
        except Exception as err:
            print(err)

    def Previous(self):
        if self.MusicNow <= 0:
            self.MusicNow = self.Total-1
        else:
            self.MusicNow -= 1
        self.LoadAndPlay()

    def Next(self):
        if self.MusicNow >= self.Total-1:
            self.MusicNow = 0
        else:
            self.MusicNow += 1
        self.LoadAndPlay()

    def Pause(self):
        mixer.music.pause()

    def Unpause(self):
        mixer.music.unpause()

    def GetMusic(self):
        return self.MusicNow

    def GetPosition(self):
        return mixer.music.get_pos()

    def GetFolder(self):
        return self.FolderPath

    def GetMusicName(self):
        return self.MusicList[self.MusicNow]
    
    def IsPlaying(self):
        return mixer.music.get_busy()

    def Exit(self):
        mixer.music.unload()
