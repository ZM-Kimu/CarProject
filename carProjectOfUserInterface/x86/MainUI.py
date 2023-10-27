from time import sleep, time
StartTime=time()  
import serial
import platform
import argparse
import tkinter as tk
import ttkbootstrap as ttk
import threading
from threading import Thread
from WidgetsProcess import Widgets,ColorGradient
from ttkbootstrap.constants import *
from ExternalFileController import Log,Config,Language

Parser = argparse.ArgumentParser(
    description="Access the control pannel faster with arguments.")
Parser.add_argument("-d", "--dev", type=str, metavar="DEVICE",
                    help="Device path of Arduino on your computer.")
Parser.add_argument("-b", "--band", type=int, metavar="BAND RATE",
                    help="Decide by band rate of Arduino.")


class Import:

    def LoadingModules(self):
        self.LoadingInfo = self.lang["Loading.Modules.Now"]
        import random
        import os
        import sys
        import ctypes
        import AudioVisual 
        from MusicPlayer import Music
        from datetime import datetime
        from tkinter import filedialog
        from AutomaticConnect import AutoCheck
        from ExternalCommunication import SerialClass, SignalSystem
        self.random=random
        self.Os=os
        self.Sys=sys
        self.Ctypes=ctypes
        self.AudioVisual=AudioVisual
        self.Music=Music()
        self.Datetime=datetime
        self.Filedialog=filedialog
        self.AutoCheck=AutoCheck
        self.SerialClass=SerialClass
        self.SignalSystem=SignalSystem
        self.LoadingInfo = self.lang["Loading.Modules.Completed"]
    

class BasicFeacture(Import):

    def ExitMain(self):
        self.Close = True
        self.RestartMain()

    def ExitNow(self):
        self.RestartMain(True)

    def RestartMain(self, exCall=False):
        if self.Restart == 0:
            self.FirstTime = time()
        self.Restart += 1
        if time()-self.FirstTime > 2:
            self.Restart = 0
        if self.Close:
            Thread(target=self.MessageBoxThread, args=("Exit Warning",
                   "To Exit the main program, you need press the Exit button 2 times.")).start()
        else:
            Thread(target=self.MessageBoxThread, args=("Restart Warning",
                   "To restart the main program, you need press the restart button 2 times.")).start()
        if self.Restart == 2:
            self.Restarted = True
            if self.Close:
                self.ReleaseResource(0)
                self.root.destroy()
                Thread(target=self.ExitThread()).start()
                self.os._exit(0)
            self.ReleaseResource(1)
            self.root.destroy()
            os.system(sys.executable+" "+sys.argv[0])
            Thread(target=self.ExitThread()).start()
        elif exCall:
            self.root.destroy()
            Thread(target=self.ExitThread()).start()
            os._exit(0)
    
    def ReleaseResource(self, Status=int):
        if Status:
            self.Widgets.StopAnimation = True
            Port = self.Port
            BandRate = self.exBandRate
            Music = self.Music.GetMusic()
            MusicTime = self.Music.GetPosition()//1000
            FolderPath = self.Music.GetFolder()
            self.Log.ChangeInitalizeStatus(
                Status, Port, BandRate, Music, MusicTime, FolderPath)
        else:
            self.Log.ChangeInitalizeStatus()

        self.Music.Exit()
        self.SerialLink.close()
        self.Log.Close()

    def ExitThread(self):
        [self.ctypes.pythonapi.PyThreadState_SetAsyncExc(x, self.ctypes.py_object(
            SystemExit)) for x, _ in threading._active.items()]

    def Communication(self, externalCall=False, BandRate=115200):
        try:
            self.Port = self.Combox.get()
            if externalCall:
                self.Port = self.exPort
            elif self.Triggle:
                self.Port = self.Log.MainInitalize()["Port"]
                BandRate = self.Log.MainInitalize()["BandRate"]
                self.MusicPlayer()
            if self.ArgInput.dev and self.ArgInput.band:
                self.Port = self.ArgInput.dev
                BandRate = self.ArgInput.band
            self.exBandRate = BandRate
            self.SerialLink = serial.Serial(self.Port, BandRate, timeout=5)
            self.Community = self.SerialClass(self.SerialLink)
            self.SignalSystem = self.SignalSystem(self.SerialLink)
            self.ConnectCompleted=True
        except Exception as err:
            Thread(target=self.MessageBoxThread,
                   args=(self.lang["Connect.Error.Title"], err, True)).start()

    def MessageBoxThread(self, Title="Not Defined Error", Text="An Error Has Been Occurented", IsBuildLog=False):
        if IsBuildLog:
            self.Log.BuildLog(Title, Text)
        Thread(target=self.Widgets.PopMessageBox, args=(Title, Text,)).start()


class OtherFeacture(BasicFeacture):

    def SceneAutoConnect(self):
        check = self.AutoCheck()
        Thread(target=check.start, args=(self.OS,)).start()
        result = 0
        while result != None:
            result = check.result
            self.LoadingInfo = check.proccess
            sleep(0.5)
        if result == None:
            Thread(target=self.MessageBoxThread, args=(
                self.lang["Connect.Auto.Error.Title"], self.lang["Connect.Auto.Error.Content"])).start()
            self.SceneOneDone=True
        else:
            self.exPort = result[0]
            exBandRate = result[1]
            self.Communication(True, exBandRate)

    def LoadingAnimation(self):
        NewInfoTime = 0
        AnimationStart = 0
        isChanged = False
        text = self.Widgets.CanvasText("", "#FFFFFF", 25, "bottom", 35, 0)
        while True:
            if self.LoadingInfo != "":
                isChanged = True
                NewInfoTime = time()
                self.BackgroundCanvas.delete(text)
                text = self.Widgets.CanvasText(
                    self.LoadingInfo, "#FFFFFF", 60, "bottom", 35, 0)
                self.LoadingInfo = ""
            if time() - AnimationStart >= 2.7 and isChanged:
                Thread(target=self.Widgets.LoadingAnime,
                       args=("bottom",)).start()
                AnimationStart = time()
            if time() - NewInfoTime >= 3 and isChanged:
                isChanged = False
                self.BackgroundCanvas.delete(text)
            sleep(0.1)

    def MusicPlayer(self):
        if self.Triggle and self.MusicStarted == False:
            self.Music.LoadAndPlay(int(self.Log.MainInitalize()["MusicNow"]), int(
                self.Log.MainInitalize()["MusicPosition"]), self.Log.MainInitalize()["MusicPath"], True)
            self.MusicStarted = True
        else:
            self.FolderPath = self.filedialog.askdirectory()
            self.Music.GetFiles(self.FolderPath)
            self.Music.LoadAndPlay()
        if self.Triggle != True:
            self.MusicController()
        Thread(target=self.Widgets.TopLineAnimation("health"))

    def MusicController(self):
        self.Widgets.Buttons("Previous", "green",
                             self.Music.Previous, 70, "left", 12, 50)
        self.Widgets.Buttons(
            "Next", "green", self.Music.Next, 70, "left", 12, 60)
        self.Widgets.Buttons(
            "Pause", "green", self.Music.Pause, 70, "left", 12, 70)
        self.Widgets.Buttons("Unpause", "green",
                             self.Music.Unpause, 70, "left", 12, 80)
        self.SongName = self.Widgets.CanvasText(
            "No song playing", "#AEA6C4", 25, "left", 12, 30)


class Scene2(OtherFeacture):

    def SceneTwoStart(self):
        try:
            Thread(target=self.SceneOneOut).start()
            Thread(target=self.Dashboard).start()
            Thread(target=self.Widgets.TopLineAnimation,
                   args=("health",)).start()
        except Exception as err:
            Thread(target=self.MessageBoxThread, args=(
                self.lang["Other.TransferToDashboard.Title"], err, True),).start()
            
    def SceneTwoIn(self):
        RestartButton = self.Widgets.Buttons(
            self.lang["Operate.Restart"], "blue", self.RestartMain, 50, "top", 5, -60)
        ExitButton = self.Widgets.Buttons(
            self.lang["Operate.Exit"], "blue", self.ExitMain, 50, "top", 5, 60)
        LeftButton = self.Widgets.Buttons(
            self.lang["Dashboard.LeftLight"], "blue", self.SignalSystem.TurnLeftSignal, 70, "left", 12, 0)
        RightButton = self.Widgets.Buttons(
            self.lang["Dashboard.RightLight"], "blue", self.SignalSystem.TurnRightSignal, 70, "right", 12, 0)
        ImportFolder = self.Widgets.Buttons(
            self.lang["Music.Import"], "red", self.MusicPlayer, 70, "left", 12, 40)
        EMERButtonGreen = self.Widgets.Buttons(
            self.lang["Dashboard.EMEROn"], "green", self.SignalSystem.AutoEmergencyLight, 80, "right", 12, 10)
        EMERButtonRed = self.Widgets.Buttons(
            self.lang["Dashboard.EMEROff"], "orange", self.SignalSystem.AutoEmergencyLight, 80, "right", 12, 10)

        testButton = ttk.Button(self.root, text="test", width=self.ScreenWidth//105, style=INFO,
                                command=self.MusicVisualize).place(x=self.ScreenWidth-self.ScreenWidth//3, y=self.ScreenHeight//50)

        EMERButtonRed.place_forget()

class SceneAutoDetect(Scene2):

    def SceneAutoDetecting(self):
        Thread(target=self.SceneOneOut).start()
        Thread(target=self.SceneAutoConnect).start()
        Thread(target=self.Widgets.TopLineAnimation, args=("health",)).start()
        Thread(target=self.SceneAutoDetectText).start()

    def SceneAutoDetectText(self):
        self.Widgets.FadeInAnime("#4A4A4A", "#FFFFFF",
                                 self.lang["Connect.Auto.Detecting1"], 150, "top", 50, 0, 0.95, True, 3)
        sleep(1.5)
        self.Widgets.FadeInAnime("#4A4A4A", "#FFFFFF",
                                 self.lang["Connect.Auto.Detecting2"], 150, "top", 50, 0, 0.95, True, 3)


class Scene1(SceneAutoDetect):

    def SceneOneIn(self):
        self.SceneOneText = self.Widgets.CanvasText(
            self.lang["Connect.Choose"], "#E1DBFF", 120, "top", 5, 0)
        self.StartButton = self.Widgets.Buttons(
            self.lang["Connect.Button"], "green", self.Communication, None, "top", 15, 0,)
        self.AutoButton = self.Widgets.Buttons(
            self.lang["Connect.Auto.Button"], "green", self.SceneAutoDetecting, 20, "top", 25, 0)
        self.Combox = ttk.Combobox(self.root, textvariable="Serial PORT")


        # Testpart
        def ttst():
            self.Widgets.Movement(self.SceneOneText,"nonlinear","place",("top",5,0),("left",30,-60),8)
            #self.Widgets.Movement(self.SceneOneText,"linear","coordinate",(0,100),(150,150),2)

        self.test111 = self.Widgets.Buttons("test", "green", ttst,20, "top", 50, 65)

        self.Combox.set("COM5")
        self.Combox["value"] = ("COM1", "COM2", "COM3", "COM4",
                                "COM5", "COM6", "COM7", "COM8", "COM9")
        if self.OS == "Linux":
            self.Combox.set("/dev/ttyACM0")
            self.Combox["value"] = ("/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3",
                                    "/dev/ttyACM4", "/dev/ttyACM5", "/dev/ttyACM6", "/dev/ttyACM7", "/dev/ttyACM8")

        self.root.protocol("WM_DELETE_WINDOW", self.ExitNow)

        if self.Log.MainInitalize()["Status"] == "1" or self.ArgInput.dev and self.ArgInput.band:
            self.Triggle = True
            self.root.after_idle(self.Communication)

        self.Widgets.Place(self.Combox, "top", 10, 0)

    def SceneOneOut(self):
        self.StartButton.place_forget()
        self.Combox.place_forget()
        self.AutoButton.place_forget()
        for i in range(0, self.ScreenHeight):
            self.BackgroundCanvas.move(self.SceneOneText, 0, -i/10000)
        self.BackgroundCanvas.delete(self.SceneOneText)
        

class SceneManager(Scene1):

    def LoadScene(self):
        while True:
            if self.SceneOneDone:
                Thread(target=self.SceneOneIn).start()
                self.SceneOneDone=False

            if self.ConnectCompleted:
                Thread(target=self.SceneTwoStart).start()
                self.ConnectCompleted=False

            sleep(0.2)
        

class Main(SceneManager):

    def __init__(self):
        self.config = Config()
        self.Log = Log()
        self.lang = Language(self.config.language).lang
        self.OS = platform.system()
        self.ArgInput = Parser.parse_args()

        self.Restart = 0
        self.LastMusicPosistion = 0
        self.ConnectCompleted=False
        self.SceneOneDone=False
        self.Close = False
        self.Triggle = False
        self.MusicStarted = False
        self.LoadingInfo=" "
        
        #self.MusicVisual = AduioVisualize()
        if Log().MainInitalize().get("MusicPosistion") != None:
            self.LastMusicPosistion = Log().MainInitalize().get("MusicPosistion")

        Thread(target=self.WindowInitialize).start()
        Thread(target=self.LoadScene).start()
        self.LoadingModules()

    def WindowInitialize(self):
        self.root = tk.Tk()
        self.root.overrideredirect(self.config.isFullScreen)
        self.ScreenWidth, self.ScreenHeight = self.root.winfo_screenwidth(
        ), self.root.winfo_screenheight()
        self.ScreenWidthMiddle, self.ScreenHeightMidddle = self.ScreenWidth//2, self.ScreenHeight//2
        ttk.Style("minty").configure(
            "TButton", font=("", self.ScreenHeight//120))
        # root.geometry(f"{ScreenWidth}x{ScreenHeight}")
        self.BackgroundCanvas = ttk.Canvas(
            self.root, width=self.ScreenWidth, height=self.ScreenHeight)
        self.Widgets = Widgets(self.root, self.ScreenWidth,
                               self.ScreenHeight, self.BackgroundCanvas)
        self.BackgroundCanvas.create_rectangle(
            0, 0, self.ScreenWidth, self.ScreenHeight, fill="#4a4a4a", outline="")

        if not self.config.OffCircles:
            for _ in range(4):
                Thread(target=self.Widgets.BackGroundCircleAnime).start()
        Thread(target=self.LoadingAnimation).start()
        

        self.BackgroundCanvas.pack()
        self.SceneOneDone=True

        EndTiming=time()
        print(EndTiming-StartTime)

        self.root.mainloop()



Main()
