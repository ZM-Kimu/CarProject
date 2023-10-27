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



class CarUI:

    def __init__(self):
        self.LoadingInfo = "Loading Modules Now"
        self.config = Config()
        self.Log = Log()
        self.OS = platform.system()
        self.ArgInput = Parser.parse_args()
        self.lang = Language(self.config.language).lang
        Thread(target=self.MainUI).start()

        self.Restart = 0
        self.Close = False
        self.Triggle = False
        self.MusicStarted = False
        self.Music = Music()
        self.MusicVisual = AduioVisualize()

        try:
            self.LastMusicPosistion = Log().MainInitalize()["MusicPosistion"]
        except:
            self.LastMusicPosistion = 0

    # Define which port need to link
    def Communication(self, externalCall=False, BandRate=115200):
        try:
            if externalCall:
                self.Port = self.exPort
            elif self.Triggle:
                self.Port = self.Log.MainInitalize()["Port"]
                BandRate = self.Log.MainInitalize()["BandRate"]
                self.MusicPlayer()
            else:
                self.Port = self.Combox.get()
            if self.ArgInput.dev and self.ArgInput.band:
                self.Port = self.ArgInput.dev
                BandRate = self.ArgInput.band
            self.exBandRate = BandRate
            self.SerialLink = serial.Serial(self.Port, BandRate, timeout=5)
            self.Community = SerialClass(self.SerialLink)
            self.SignalSystem = SignalSystem(self.SerialLink)
            self.TransToDashboardTreads()
        except Exception as err:
            Thread(target=self.MessageBoxThread,
                   args=(self.lang["Connect.Error.Title"], err, True)).start()

    # Define the start interface, used to link communication port
    def MainUI(self):
        self.root = tk.Tk()
        # self.root.overrideredirect(True)
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

        self.FirstText = self.Widgets.CanvasText(
            self.lang["Connect.Choose"], "#E1DBFF", 120, "top", 5, 0)
        self.StartButton = self.Widgets.Buttons(
            self.lang["Connect.Button"], "green", self.Communication, None, "top", 15, 0,)
        self.AutoButton = self.Widgets.Buttons(
            self.lang["Connect.Auto.Button"], "green", self.AutoConnect, 20, "top", 25, 0)
        self.Combox = ttk.Combobox(self.root, textvariable="Serial PORT")

        if self.OS == "Windows":
            self.Combox.set("COM5")
            self.Combox["value"] = ("COM1", "COM2", "COM3", "COM4",
                                    "COM5", "COM6", "COM7", "COM8", "COM9")
        elif self.OS == "Linux":
            self.Combox.set("/dev/ttyACM0")
            self.Combox["value"] = ("/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3",
                                    "/dev/ttyACM4", "/dev/ttyACM5", "/dev/ttyACM6", "/dev/ttyACM7", "/dev/ttyACM8")
        if not self.config.OffCircles:
            for _ in range(4):
                Thread(target=self.Widgets.BackGroundAnime).start()

        self.Widgets.Place(self.Combox, "top", 10, 0)
        self.BackgroundCanvas.pack()

        Thread(target=self.LoadingAnimation).start()

        # Testpart

        # self.test111 = self.Widgets.Buttons("test", "green", ttest,20, "top", 50, 65)

        self.root.protocol("WM_DELETE_WINDOW", self.ExitNow)

        if self.Log.MainInitalize()["Status"] == "1" or self.ArgInput.dev and self.ArgInput.band:
            self.Triggle = True
            self.root.after_idle(self.Communication)

        self.root.mainloop()

    def Dashboard(self):
        # TODO:Accelerator,Turnning...
        try:
            KmLabelLeft = self.Widgets.CanvasText(
                "KM/H", "#E3BCD3", 150, "top", 80, -120)
            KmLabelRight = self.Widgets.CanvasText(
                "KM/H", "#E3BCD3", 150, "top", 80, 120)
            SpeedLeft = self.Widgets.CanvasText(
                "0", "#EDA69F", 188, "top", -20, -70)
            SpeedRight = self.Widgets.CanvasText(
                "0", "#EDA69F", 188, "top", -20, 70)

            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(KmLabelLeft, i/3650, 0)
            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(KmLabelRight, -i/3650, 0)
            for i in range(self.ScreenHeight, 0, -1):
                self.BackgroundCanvas.move(SpeedLeft, 0, i/2400)
            for i in range(self.ScreenHeight, 0, -1):
                self.BackgroundCanvas.move(SpeedRight, 0, i/2400)

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
            
            if self.Triggle:
                self.MusicController()

            ReadList = {'SLeft': 0, 'SRight': 0,
                        'Pow': 0, 'Accel': 0, 'Status': 0, 'CmdCode': '-1'}
            LastFlushTime = 0
            while True:

                print([(x, _) for x, _ in threading._active.items()])
                reading = self.Community.readBinary()

                if self.Music.GetPosition() == -1 and self.Music.MusicList:
                    self.Music.Next()
                if time()-LastFlushTime > 1.2:
                    if reading != None:
                        ReadList = reading
                    self.BackgroundCanvas.delete(KmLabelLeft)
                    self.BackgroundCanvas.delete(KmLabelRight)
                    self.BackgroundCanvas.delete(SpeedLeft)
                    self.BackgroundCanvas.delete(SpeedRight)
                    KmLabelLeft = self.Widgets.CanvasText(
                        "KM/H", "#E3BCD3", 150, "top", 80, -50)
                    KmLabelRight = self.Widgets.CanvasText(
                        "KM/H", "#E3BCD3", 150, "top", 80, 50)
                    SpeedLeft = self.Widgets.CanvasText(
                        ReadList["SLeft"], "#EDA69F", 188, "top", 40, -70)
                    SpeedRight = self.Widgets.CanvasText(
                        ReadList["SRight"], "#EDA69F", 188, "top", 40, 70)

                    if ReadList["CmdCode"] == "01" and not EMERButtonRed.winfo_ismapped() and EMERButtonGreen.winfo_ismapped():
                        EMERButtonGreen.place_forget()
                        self.Widgets.Place(EMERButtonRed, "right", 12, 10)
                    elif ReadList["CmdCode"] != "01" and EMERButtonRed.winfo_ismapped() and not EMERButtonGreen.winfo_ismapped():
                        EMERButtonRed.place_forget()
                        self.Widgets.Place(EMERButtonGreen, "right", 12, 10)
                    LastFlushTime = time()

                if time()-self.SignalSystem.CommandSendTime > 1.5:
                    if ReadList["CmdCode"] != self.SignalSystem.SignalCode and self.SignalSystem.CommandIsSended:
                        self.SignalSystem.CodeSignal(
                            self.SignalSystem.SignalCode)
                    if ReadList["CmdCode"] == self.SignalSystem.SignalCode:
                        self.SignalSystem.CommandIsSended = False

                if self.Music.IsPlaying():
                    self.BackgroundCanvas.delete(self.SongName)
                    self.SongName = self.Widgets.CanvasText(
                        self.Music.GetMusicName(), "#AEA6C4", 18, "left", 12, 30, self.ScreenWidth//12)
        except Exception as err:
            Thread(target=self.MessageBoxThread, args=(
                "Dashboard Error", err, True)).start()

    def MessageBoxThread(self, Title="Not Defined Error", Text="An Error Has Been Occurented", IsBuildLog=False):
        if IsBuildLog:
            self.Log.BuildLog(Title, Text)
        Thread(target=self.Widgets.PopMessageBox, args=(Title, Text,)).start()

    def AutoProcess(self):
        check = AutoCheck()
        Thread(target=check.start, args=(self.OS,)).start()
        result = 0
        while result != None:
            result = check.result
            self.LoadingInfo = check.proccess
            sleep(0.5)
        if result == None:
            Thread(target=self.MessageBoxThread, args=(
                self.lang["Connect.Auto.Error.Title"], self.lang["Connect.Auto.Error.Content"])).start()
            self.FirstText = self.Widgets.CanvasText(
                self.lang["Connect.Choose"], "#E1DBFF", 80, "top", 5, 0)
            self.Widgets.Place(self.Combox, "top", 10, 0)
            self.Widgets.Place(self.StartButton, "top", 15, 0)
            self.Widgets.Place(self.AutoButton, "top", 25, 0)
        else:
            self.exPort = result[0]
            exBandRate = result[1]
            self.Communication(True, exBandRate)

    def AutoText(self):
        self.Widgets.FadeInAnime("#4A4A4A", "#FFFFFF",
                                 self.lang["Connect.Auto.Detecting1"], 150, "top", 50, 0, 0.95, True, 3)
        sleep(1.5)
        self.Widgets.FadeInAnime("#4A4A4A", "#FFFFFF",
                                 self.lang["Connect.Auto.Detecting2"], 150, "top", 50, 0, 0.95, True, 3)

    def AutoConnect(self):
        Thread(target=self.LinkPageFade).start()
        Thread(target=self.AutoProcess).start()
        Thread(target=self.Widgets.TopLineAnimation, args=("health",)).start()
        Thread(target=self.AutoText).start()

    def LinkPageFade(self):
        self.StartButton.place_forget()
        self.Combox.place_forget()
        self.AutoButton.place_forget()
        for i in range(0, self.ScreenHeight):
            self.BackgroundCanvas.move(self.FirstText, 0, -i/10000)
        self.BackgroundCanvas.delete(self.FirstText)

    def TransToDashboardTreads(self):
        try:
            Thread(target=self.LinkPageFade).start()
            Thread(target=self.Dashboard).start()
            Thread(target=self.Widgets.TopLineAnimation,
                   args=("health",)).start()
        except Exception as err:
            Thread(target=self.MessageBoxThread, args=(
                self.lang["Other.TransferToDashboard.Title"], err, True),).start()

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

    def SendMessage(self, args):
        self.Message = {'Status': 1}
        self.Community.ProtocalSend(args=self.Message)

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
                os._exit(0)
            else:
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
        [ctypes.pythonapi.PyThreadState_SetAsyncExc(x, ctypes.py_object(
            SystemExit)) for x, _ in threading._active.items()]

    def MusicPlayer(self):
        if self.Triggle and self.MusicStarted == False:
            self.Music.LoadAndPlay(int(self.Log.MainInitalize()["MusicNow"]), int(
                self.Log.MainInitalize()["MusicPosition"]), self.Log.MainInitalize()["MusicPath"], True)
            self.MusicStarted = True
        else:
            self.FolderPath = filedialog.askdirectory()
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

    def MusicVisualize(self):

        def Visual():
            # TODO:Complete the action after a song end
            self.MusicVisual.MainAnalyze(
                self.Music.FolderPath+"/"+self.Music.MusicList[self.Music.MusicNow], self.ScreenWidth, self.ScreenHeight)

            getTicksLastFrame = 0
            radius = self.MusicVisual.radius
            poly_color = self.MusicVisual.poly_color
            bass_trigger = self.MusicVisual.bass_trigger
            polygon_default_color = self.MusicVisual.polygon_default_color
            polygon_bass_color = self.MusicVisual.polygon_bass_color
            polygon_color_vel = self.MusicVisual.polygon_color_vel
            bass_trigger_started = self.MusicVisual.bass_trigger_started

            min_radius = self.MusicVisual.min_radius
            max_radius = self.MusicVisual.max_radius
            min_decibel = self.MusicVisual.min_decibel
            max_decibel = self.MusicVisual.max_decibel

            PolygonCanvas = self.BackgroundCanvas.create_polygon(0, 0, 0, 0)
            CircleCanvas = self.BackgroundCanvas.create_oval(0, 0, 0, 0)
            running = True
            while running:

                avg_bass = 0
                self.MusicVisual.poly = []

                t = self.Music.GetPosition()
                deltaTime = (t - getTicksLastFrame) / 1000.0
                getTicksLastFrame = t

                if self.Music.IsPlaying() == False:
                    running = False

                for b1 in self.MusicVisual.bars:
                    for b in b1:
                        b.update_all(
                            deltaTime, self.Music.GetPosition() / 1000.0, self.MusicVisual.analyzer)

                # b为bars内的第一个实例，即低音频率类，由于self.avg已经由上方的update_all方法改变，因此在时间点是有效的
                for b in self.MusicVisual.bars[0]:
                    avg_bass += b.avg  # 获取在某时间点下的低音频率类的平均分贝

                avg_bass /= len(self.MusicVisual.bars[0])  # 将低音频率类的值归细

                if avg_bass > bass_trigger:
                    # 以下代码块控制在低音触发下的图形的整体缩放
                    if bass_trigger_started == 0:
                        bass_trigger_started = self.Music.GetPosition()  # 得到低音时的时间
                    if (self.Music.GetPosition() - bass_trigger_started)/1000.0 > 2:  # （例外情况）
                        polygon_bass_color = rnd_color()
                        bass_trigger_started = 0
                    if polygon_bass_color is None:  # （例外情况）
                        polygon_bass_color = rnd_color()
                    # 将分贝范围与圆范围进行匹配，并得出经过低音振幅大小后的新直径
                    newr = min_radius + int(avg_bass * ((max_radius - min_radius) /
                                            (max_decibel - min_decibel)) + (max_radius - min_radius))
                    # 半径需要移动的距离的宏观化
                    radius_vel = (newr - radius) / 0.15
                    # 在低音触发后淡出时的颜色改变
                    polygon_color_vel = [
                        (polygon_bass_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]
                # 当不处于低音触发时，如果现在的图形状态大于默认状态；即控制低音触发后进行动画收回的代码块
                elif radius > min_radius:
                    bass_trigger_started = 0
                    polygon_bass_color = None
                    radius_vel = (self.MusicVisual.min_radius - radius) / 0.15
                    polygon_color_vel = [
                        (polygon_default_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]
                # 在未被低音触发或从触发恢复的正常态下，图形大小保持默认值
                else:
                    bass_trigger_started = 0
                    poly_color = polygon_default_color.copy()
                    polygon_bass_color = None
                    polygon_color_vel = [0, 0, 0]

                    radius_vel = 0
                    radius = min_radius

                # 在每次循环加上半径变化值乘上时间状态经过的值，有助于非线性变化
                radius += radius_vel * deltaTime

                # 用以处理颜色渐变
                for x in range(len(polygon_color_vel)):
                    value = polygon_color_vel[x]*deltaTime + poly_color[x]
                    poly_color[x] = value

                # 获取在bars内每个实例对象的x与y的坐标
                for b1 in self.MusicVisual.bars:
                    for b in b1:
                        # 可通过调参更改柱状的倾角
                        b.x, b.y = self.MusicVisual.circleX+radius * math.cos(math.radians(
                            b.angle - 200)), self.MusicVisual.circleY + radius * math.sin(math.radians(b.angle - 200))
                        b.update_rect()

                        # 在此append方法中，poly只关心目标坐标，即柱状高度
                        self.MusicVisual.poly.append(b.rect.points[3])
                        self.MusicVisual.poly.append(b.rect.points[2])

                self.BackgroundCanvas.delete(PolygonCanvas, CircleCanvas)
                PolygonCanvas = self.BackgroundCanvas.create_polygon(
                    self.MusicVisual.poly, fill=rgb2hex(poly_color))
                CircleCanvas = self.BackgroundCanvas.create_oval(self.ScreenWidth/2-int(radius)/1.5+5, self.ScreenHeight/2-int(
                    radius)/1.5, self.ScreenWidth/2+int(radius)/1.5+5, self.ScreenHeight/2+int(radius)/1.5, fill="#4a4a4a", outline="")
        Thread(target=Visual).start()

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
            if externalCall:
                self.Port = self.exPort
            elif self.Triggle:
                self.Port = self.Log.MainInitalize()["Port"]
                BandRate = self.Log.MainInitalize()["BandRate"]
                self.MusicPlayer()
            else:
                self.Port = self.Combox.get()
            if self.ArgInput.dev and self.ArgInput.band:
                self.Port = self.ArgInput.dev
                BandRate = self.ArgInput.band
            self.exBandRate = BandRate
            self.SerialLink = serial.Serial(self.Port, BandRate, timeout=5)
            self.Community = SerialClass(self.SerialLink)
            self.SignalSystem = SignalSystem(self.SerialLink)
            self.TransToDashboardTreads()
        except Exception as err:
            Thread(target=self.MessageBoxThread,
                   args=(self.lang["Connect.Error.Title"], err, True)).start()

    def MessageBoxThread(self, Title="Not Defined Error", Text="An Error Has Been Occurented", IsBuildLog=False):
        if IsBuildLog:
            self.Log.BuildLog(Title, Text)
        Thread(target=self.Widgets.PopMessageBox, args=(Title, Text,)).start()


class OtherFeacture(BasicFeacture):

    def AutoConnect(self):
        Thread(target=self.LinkPageFade).start()
        Thread(target=self.AutoProcess).start()
        Thread(target=self.Widgets.TopLineAnimation, args=("health",)).start()
        Thread(target=self.AutoText).start()

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
    pass


class Scene1(Scene2):

    def SceneOne(self):

        self.FirstText = self.Widgets.CanvasText(
            self.lang["Connect.Choose"], "#E1DBFF", 120, "top", 5, 0)
        self.StartButton = self.Widgets.Buttons(
            self.lang["Connect.Button"], "green", self.Communication, None, "top", 15, 0,)
        self.AutoButton = self.Widgets.Buttons(
            self.lang["Connect.Auto.Button"], "green", self.AutoConnect, 20, "top", 25, 0)
        self.Combox = ttk.Combobox(self.root, textvariable="Serial PORT")

        self.Combox.set("COM5")
        self.Combox["value"] = ("COM1", "COM2", "COM3", "COM4",
                                "COM5", "COM6", "COM7", "COM8", "COM9")
        if self.OS == "Linux":
            self.Combox.set("/dev/ttyACM0")
            self.Combox["value"] = ("/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3",
                                    "/dev/ttyACM4", "/dev/ttyACM5", "/dev/ttyACM6", "/dev/ttyACM7", "/dev/ttyACM8")
            

        Thread(target=self.LoadingAnimation).start()

        # Testpart
        # self.test111 = self.Widgets.Buttons("test", "green", ttest,20, "top", 50, 65)

        self.root.protocol("WM_DELETE_WINDOW", self.ExitNow)

        if self.Log.MainInitalize()["Status"] == "1" or self.ArgInput.dev and self.ArgInput.band:
            self.Triggle = True
            self.root.after_idle(self.Communication)

        self.Widgets.Place(self.Combox, "top", 10, 0)


class SceneManager(Scene1):

    def LoadSceneOne(self):
        while True:
            if self.SceneOneDone:
                self.SceneOne()
                break


class Main(SceneManager):

    def __init__(self):
        self.config = Config()
        self.Log = Log()
        self.lang = Language(self.config.language).lang
        self.OS = platform.system()
        self.ArgInput = Parser.parse_args()

        self.Restart = 0
        self.LastMusicPosistion = 0
        self.SceneOneDone=False
        self.Close = False
        self.Triggle = False
        self.MusicStarted = False
        
        #self.MusicVisual = AduioVisualize()
        if Log().MainInitalize().get("MusicPosistion") != None:
            self.LastMusicPosistion = Log().MainInitalize().get("MusicPosistion")

        Thread(target=self.WindowInitialize).start()
        Thread(target=self.LoadSceneOne).start()
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
                Thread(target=self.Widgets.BackGroundAnime).start()

        self.BackgroundCanvas.pack()
        self.SceneOneDone=True

        EndTiming=time()
        print(EndTiming-StartTime)

        self.root.mainloop()



def Import():
    pass

# CarUI()

Main()
