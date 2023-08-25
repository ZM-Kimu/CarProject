import serial
import random
import time
import os
import sys
import tkinter as tk
import ttkbootstrap as ttk
from threading import Thread
from LogSystem import Log
from AudioVisual import *
from datetime import datetime
from MusicPlayer import Music
from tkinter import filedialog
from ttkbootstrap.constants import *
from ColorChange import animationObj
from ExternalCommunication import SerialClass



class CarUI:

    def __init__(self):
        self.Restart = 0
        self.Close = False
        self.Triggle = False
        self.MusicStarted = False
        self.Log = Log()
        self.Music = Music()
        self.MusicVisual=AduioVisualize()
        try:
            self.LastMusicPosistion=Log().MainInitalize()["MusicPosistion"]
        except:
            self.LastMusicPosistion=0
        self.MainUI()

    # Define which port need to link
    def Communication(self):
        try:
            if self.Triggle:
                self.Port = self.Log.MainInitalize()["Port"]
                self.MusicPlayer()

            else:
                self.Port = self.Combox.get()
            self.SerialLink = serial.Serial(self.Port, 115200, timeout=10)
            self.Community = SerialClass(self.SerialLink)
            self.TransToDashboardTreads()
        except Exception as err:
            Thread(target=self.MessageBoxThread,
                   args=("Connect Error", err)).start()

    # Define the start interface, used to link communication port
    def MainUI(self):
        self.root = tk.Tk()
        # self.root.overrideredirect(True)
        self.ScreenWidth, self.ScreenHeight = self.root.winfo_screenwidth(
        ), self.root.winfo_screenheight()
        self.ScreenWidthMiddle, self.ScreenHeightMidddle = self.ScreenWidth//2, self.ScreenHeight//2
        ttk.Style("minty").configure("TButton",font=("",self.ScreenHeight//120))
        # root.geometry(f"{ScreenWidth}x{ScreenHeight}")

        self.BackgroundCanvas = ttk.Canvas(
            self.root, width=self.ScreenWidth, height=self.ScreenHeight)
        self.StartButton = ttk.Button(
            self.root, text="Start!", command=self.Communication)
        self.Combox = ttk.Combobox(self.root, textvariable="COM PORT")
        self.Combox.set("COM5")
        self.Combox["value"] = ("COM1", "COM2", "COM3", "COM4",
                                "COM5", "COM6", "COM7", "COM8", "COM9")

        self.BackgroundCanvas.create_rectangle(
            0, 0, self.ScreenWidth, self.ScreenHeight, fill="#4a4a4a", outline="")
        self.LabelLink = self.BackgroundCanvas.create_text(self.ScreenWidthMiddle-self.ScreenWidthMiddle//50, self.ScreenHeight //
                                                           75, text="Please choose the serial port", font=("", self.ScreenHeight//40), fill="#E1DBFF")

        for _ in range(4):
            Thread(target=self.CanvasCircle).start()

        self.Combox.place(x=self.ScreenWidthMiddle -
                          self.ScreenWidthMiddle // 22, y=self.ScreenHeight//25)
        self.StartButton.place(
            x=self.ScreenWidthMiddle-self.ScreenWidthMiddle // 50, y=self.ScreenHeight//12)
        self.BackgroundCanvas.pack()

        if self.Log.MainInitalize()["Status"] == "1":
            self.Triggle = True
            self.root.after_idle(self.Communication)

        self.root.mainloop()

    def Dashboard(self):
        try:
            KmLabelLeft = self.BackgroundCanvas.create_text(-self.ScreenWidth//30, self.ScreenHeight //
                                                            3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
            KmLabelRight = self.BackgroundCanvas.create_text(
                self.ScreenWidth*1.1, self.ScreenHeight//3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
            self.SpeedLeft = self.BackgroundCanvas.create_text(
                self.ScreenWidth//7, -self.ScreenHeight//4, text="0", font=("", self.ScreenHeight//8), fill="#EDA69F")
            self.SpeedRight = self.BackgroundCanvas.create_text(
                self.ScreenWidth-self.ScreenWidth//5, -self.ScreenHeight // 4, text="0", font=("", self.ScreenHeight//8), fill="#EDA69F")

            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(KmLabelLeft, i/4500, 0)
            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(KmLabelRight, -i/3200, 0)
            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(self.SpeedLeft, 0, i/5000)
            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(self.SpeedRight, 0, i/5000)

            RestartButton = ttk.Button(self.root, text="Restart", width=self.ScreenWidth//105, style=INFO,
                                       command=self.RestartMain).place(x=self.ScreenWidth//5, y=self.ScreenHeight//50)
            CloseButton = ttk.Button(self.root, text="Exit", width=self.ScreenWidth//105, style=INFO,
                                     command=self.ExitMain,).place(x=self.ScreenWidth-self.ScreenWidth//4, y=self.ScreenHeight//50)
            ImportFolder = ttk.Button(self.root, text="ImportMusic", width=self.ScreenWidth//130, style=SECONDARY,
                                      command=self.MusicPlayer,).place(x=self.ScreenWidth//50, y=self.ScreenHeight*0.7)
            testButton = ttk.Button(self.root, text="test", width=self.ScreenWidth//105, style=INFO,
                                    command=Thread(target=self.StartMusicVisualize).start,).place(x=self.ScreenWidth-self.ScreenWidth//3, y=self.ScreenHeight//50)
            if self.Triggle:
                self.MusicController()

            while True:
                reading = self.Community.readBinary()
                self.SendMessage()
                time.sleep(1)
                if self.Music.GetPosition() == -1:
                    self.Music.Next()
            

                if reading != None:
                    ReadList = reading
                self.BackgroundCanvas.delete(KmLabelLeft)
                self.BackgroundCanvas.delete(KmLabelRight)
                self.BackgroundCanvas.delete(self.SpeedLeft)
                self.BackgroundCanvas.delete(self.SpeedRight)
                KmLabelLeft = self.BackgroundCanvas.create_text(
                    self.ScreenWidth//4, self.ScreenHeight//3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
                KmLabelRight = self.BackgroundCanvas.create_text(
                    self.ScreenWidth-self.ScreenWidth//3.35, self.ScreenHeight//3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
                self.SpeedLeft = self.BackgroundCanvas.create_text(self.ScreenWidth//7, self.ScreenHeight//5, text=ReadList[
                    "SpeedLeft"], font=("", self.ScreenHeight//8), fill="#EDA69F")
                self.SpeedRight = self.BackgroundCanvas.create_text(self.ScreenWidth-self.ScreenWidth//5, self.ScreenHeight//5, text=ReadList[
                    "SpeedRight"], font=("", self.ScreenHeight//8), fill="#EDA69F")
                
                if self.Music.IsPlaying():
                    self.BackgroundCanvas.delete(self.SongName)
                    self.SongName = self.BackgroundCanvas.create_text(
                        self.ScreenWidth//18, self.ScreenHeight*0.65, text=self.Music.GetMusicName(), font=("", self.ScreenHeight//120),width=self.ScreenWidth//12, fill="#AEA6C4")
        except Exception as err:
            Thread(target=self.MessageBoxThread, args=(
                "Dashboard Error", err)).start()

    def TopLineAnimation(self, status, bgcolor="#4A4A4A"):
        try:
            if status == "health":
                FillColor = "#8CC9C8"
            if status == "warning":
                FillColor = "#F510CA"
            if status == "emergency":
                FillColor = "#FF0000"
            startPointL = self.ScreenWidth/2
            startPointR = self.ScreenWidth/2
            y = 0
            offset = 0
            tick = 0
            change = animationObj(FillColor, bgcolor).gradient()
            while True:
                self.BackgroundCanvas.delete("line")
                if startPointR < self.ScreenWidth-self.ScreenWidth/5:
                    line = self.BackgroundCanvas.create_line(
                        startPointL, y, startPointR, y, fill=FillColor, width=4)
                else:
                    self.BackgroundCanvas.delete(line)
                    line = self.BackgroundCanvas.create_line(
                        startPointL, y, startPointR, y, fill=change[tick], width=4)
                    tick += 1
                    if tick >= len(change)-1:
                        break
                startPointL -= offset
                startPointR += offset
                offset += 1
                self.BackgroundCanvas.update()
        except:
            pass

    def MessageBoxThread(self, Title="Not Defined Error", Text="An Error Has Been Occurented"):
        try:
            x1, y1, x2, y2 = self.ScreenWidth*1.3-self.ScreenWidth//5, self.ScreenHeight - \
                self.ScreenHeight//4, self.ScreenWidth*1.3 - \
                self.ScreenWidth//60, self.ScreenHeight-self.ScreenHeight//15
            r = 25
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2,
                      y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            self.MessageFrame = self.BackgroundCanvas.create_polygon(
                points, smooth=True, outline="", fill="#FFFFFF")
            self.MessageTitle = self.BackgroundCanvas.create_text(
                self.ScreenWidth*1.2, self.ScreenHeight-self.ScreenHeight//4.4, text=Title, font=("", self.ScreenHeight//75), width=self.ScreenWidth//6, fill="#757575")
            self.MessageText = self.BackgroundCanvas.create_text(
                self.ScreenWidth*1.2, self.ScreenHeight-self.ScreenHeight//7, text=Text, font=("", self.ScreenHeight//85), width=self.ScreenWidth//6, fill="#212121")
            self.Log.BuildLog(Title, Text)
            Thread(target=self.MessageBoxAnimation).start()
        except Exception as err:
            print(err)

    def MessageBoxAnimation(self):
        for i in range(self.ScreenWidth//7, 0, -1):
            self.BackgroundCanvas.move(self.MessageFrame, -i/87, 0)
            self.BackgroundCanvas.move(self.MessageTitle, -i/85, 0)
            self.BackgroundCanvas.move(self.MessageText, -i/85, 0)
        time.sleep(2)
        for i in range(0, self.ScreenWidth//7):
            self.BackgroundCanvas.move(self.MessageFrame, i/87, 0)
            self.BackgroundCanvas.move(self.MessageTitle, i/85, 0)
            self.BackgroundCanvas.move(self.MessageText, i/85, 0)
        self.BackgroundCanvas.delete(
            self.MessageFrame, self.MessageTitle, self.MessageText)

    def CanvasCircle(self):
        try:
            while True:
                StartMovementWidth = random.randint(
                    self.ScreenWidth//15, self.ScreenWidth)
                StartMovementHeight = random.randint(
                    self.ScreenHeight//15, self.ScreenHeight)
                EndMovementWidth = random.randint(
                    self.ScreenWidth//18, self.ScreenWidth-self.ScreenWidth//3)
                EndMovementHeight = random.randint(
                    self.ScreenHeight//18, self.ScreenHeight-self.ScreenHeight//3)
                MoveWidthValue = self.ScreenWidth/8000
                MoveHeightValue = self.ScreenHeight/8000
                self.BackgroundCanvas.update()
                IsChange = True
                X1, Y1, X2, Y2 = StartMovementWidth, StartMovementHeight, StartMovementWidth + \
                    self.ScreenWidth//3, StartMovementHeight+self.ScreenWidth//3
                tick = 0
                oval = self.BackgroundCanvas.create_oval(
                    X1, Y1, X2, Y2, fill="#505061", outline="")
                while True:
                    PosistionNow = self.BackgroundCanvas.coords(oval)
                    if PosistionNow[0] <= EndMovementWidth and IsChange:
                        MoveWidthValue = -MoveWidthValue
                        IsChange = False
                    if PosistionNow[1] <= EndMovementWidth and IsChange:
                        MoveHeightValue = -MoveHeightValue
                        IsChange = False
                    if abs(PosistionNow[0] - EndMovementWidth) <= self.ScreenWidth//7000 or abs(PosistionNow[1] - EndMovementHeight) <= self.ScreenHeight//7000 or abs(PosistionNow[0]) >= self.ScreenWidth*1.1 or abs(PosistionNow[1]) >= self.ScreenHeight*1.1 or tick >= 10000:
                        break
                    self.BackgroundCanvas.move(
                        oval, MoveWidthValue, MoveHeightValue)
                    self.BackgroundCanvas.update()
                    tick += 1
        except:
            pass

    def LinkPageFade(self):
        self.StartButton.place_forget()
        self.Combox.place_forget()
        for i in range(0, self.ScreenHeight):
            self.BackgroundCanvas.move(self.LabelLink, 0, -i/10000)
        self.BackgroundCanvas.delete(self.LabelLink)

    def TransToDashboardTreads(self):
        try:
            Thread(target=self.LinkPageFade).start()
            Thread(target=self.Dashboard).start()
            Thread(target=self.TopLineAnimation, args=("health",)).start()
        except Exception as err:
            pass
            Thread(target=self.MessageBoxThread, args=(
                "Transfer to dashboard Error", err)).start()

    def SendMessage(self):
        args = {'Status': 1, 'Operation': 'yes'}
        self.Community.ProtocalSend(args=args)

    def ExitMain(self):
        self.Close = True
        self.RestartMain()

    def RestartMain(self):
        if self.Restart == 0:
            self.FirstTime = time.time()
        self.Restart += 1
        if time.time()-self.FirstTime > 2:
            self.Restart = 0
        if self.Close:
            Thread(target=self.MessageBoxThread, args=("Restart Warning",
                   "To Exit the main program, you need to press the Exit button for 2 times.")).start()
        else:
            Thread(target=self.MessageBoxThread, args=("Restart Warning",
                   "To restart the main program, you need to press the restart button for 2 times.")).start()
        if self.Restart == 2:
            self.Restarted = True
            if self.Close:
                self.ReleaseResource(0)
                os._exit(0)
            else:
                self.ReleaseResource(1)
                self.root.destroy()
                os.system(sys.executable+" "+sys.argv[0])
                new = CarUI().Communication()
                new.Communication()

    def ReleaseResource(self, Status=int):
        if Status:
            Port = self.Port
            Music = self.Music.GetMusic()
            MusicTime = self.Music.GetPosition()//1000
            FolderPath = self.Music.GetFolder()
            self.Log.ChangeInitalizeStatus(
                Status, Port, Music, MusicTime, FolderPath)
        else:
            self.Log.ChangeInitalizeStatus()
        self.Music.Exit()
        self.SerialLink.close()
        self.Log.Close()

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
        Thread(target=self.TopLineAnimation("health"))

    def MusicController(self):
        ttk.Button(self.root, text="Previous", width=self.ScreenWidth//130, style=SUCCESS,
                   command=self.Music.Previous,).place(x=self.ScreenWidth//50, y=self.ScreenHeight*0.75)
        ttk.Button(self.root, text="Next", width=self.ScreenWidth//130, style=SUCCESS,
                   command=self.Music.Next,).place(x=self.ScreenWidth//50, y=self.ScreenHeight*0.8)
        ttk.Button(self.root, text="Pause", width=self.ScreenWidth//130, style=SUCCESS,
                   command=self.Music.Pause,).place(x=self.ScreenWidth//50, y=self.ScreenHeight*0.85)
        ttk.Button(self.root, text="Unpause", width=self.ScreenWidth//130, style=SUCCESS,
                   command=self.Music.Unpause,).place(x=self.ScreenWidth//50, y=self.ScreenHeight*0.9)
        self.SongName = self.BackgroundCanvas.create_text(
            self.ScreenWidth//23, self.ScreenHeight*0.65, text="No song playing", font=("", self.ScreenHeight//120), fill="#AEA6C4")
        
    def StartMusicVisualize(self):
        Thread(target=self.MusicVisualize).start()

        
    def MusicVisualize(self):
        self.MusicVisual.MainAnalyze(self.Music.FolderPath+"/"+self.Music.MusicList[self.Music.MusicNow],self.ScreenWidth,self.ScreenHeight)

        getTicksLastFrame=0
        radius=self.MusicVisual.radius
        poly_color=self.MusicVisual.poly_color
        bass_trigger=self.MusicVisual.bass_trigger
        polygon_default_color=self.MusicVisual.polygon_default_color
        polygon_bass_color=self.MusicVisual.polygon_bass_color
        polygon_color_vel=self.MusicVisual.polygon_color_vel
        bass_trigger_started=self.MusicVisual.bass_trigger_started

        min_radius=self.MusicVisual.min_radius
        max_radius=self.MusicVisual.max_radius
        min_decibel=self.MusicVisual.min_decibel
        max_decibel=self.MusicVisual.max_decibel

        PolygonCanvas=self.BackgroundCanvas.create_polygon(0,0,0,0)
        CircleCanvas=self.BackgroundCanvas.create_oval(0,0,0,0)
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

            #b为bars内的第一个实例，即低音频率类，由于self.avg已经由上方的update_all方法改变，因此在时间点是有效的
            for b in self.MusicVisual.bars[0]:
                avg_bass += b.avg#获取在某时间点下的低音频率类的平均分贝

            avg_bass /= len(self.MusicVisual.bars[0])#将低音频率类的值归细

            if avg_bass > bass_trigger:
                #以下代码块控制在低音触发下的图形的整体缩放
                if bass_trigger_started == 0:
                    bass_trigger_started = self.Music.GetPosition()#得到低音时的时间
                if (self.Music.GetPosition() - bass_trigger_started)/1000.0 > 2:#（例外情况）
                    polygon_bass_color = rnd_color()
                    bass_trigger_started = 0
                if polygon_bass_color is None:#（例外情况）
                    polygon_bass_color = rnd_color()
                #将分贝范围与圆范围进行匹配，并得出经过低音振幅大小后的新直径
                newr = min_radius + int(avg_bass * ((max_radius - min_radius) /
                                        (max_decibel - min_decibel)) + (max_radius - min_radius))
                #半径需要移动的距离的宏观化
                radius_vel = (newr - radius) / 0.15
                #在低音触发后淡出时的颜色改变
                polygon_color_vel = [
                    (polygon_bass_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]
            #当不处于低音触发时，如果现在的图形状态大于默认状态；即控制低音触发后进行动画收回的代码块
            elif radius > min_radius:
                bass_trigger_started = 0
                polygon_bass_color = None
                radius_vel = (self.MusicVisual.min_radius - radius) / 0.15
                polygon_color_vel = [
                    (polygon_default_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]
            #在未被低音触发或从触发恢复的正常态下，图形大小保持默认值
            else:
                bass_trigger_started = 0
                poly_color = polygon_default_color.copy()
                polygon_bass_color = None
                polygon_color_vel = [0, 0, 0]

                radius_vel = 0
                radius = min_radius

            #在每次循环加上半径变化值乘上时间状态经过的值，有助于非线性变化
            radius += radius_vel * deltaTime

            #用以处理颜色渐变
            for x in range(len(polygon_color_vel)):
                value = polygon_color_vel[x]*deltaTime + poly_color[x]
                poly_color[x] = value

            #获取在bars内每个实例对象的x与y的坐标
            for b1 in self.MusicVisual.bars:
                for b in b1:
                    #可通过调参更改柱状的倾角
                    b.x, b.y = self.MusicVisual.circleX+radius * math.cos(math.radians(b.angle - 200)), self.MusicVisual.circleY + radius * math.sin(math.radians(b.angle - 200))
                    b.update_rect()

                    #在此append方法中，poly只关心目标坐标，即柱状高度
                    self.MusicVisual.poly.append(b.rect.points[3])
                    self.MusicVisual.poly.append(b.rect.points[2])

            self.BackgroundCanvas.delete(PolygonCanvas,CircleCanvas)
            PolygonCanvas=self.BackgroundCanvas.create_polygon(self.MusicVisual.poly,fill=rgb2hex(poly_color))
            CircleCanvas=self.BackgroundCanvas.create_oval(self.ScreenWidth/2-int(radius)/1.5+5,self.ScreenHeight/2-int(radius)/1.5,self.ScreenWidth/2+int(radius)/1.5+5,self.ScreenHeight/2+int(radius)/1.5,fill="#4a4a4a",outline="")



CarUI()
