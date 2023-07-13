import serial
import random
import time
import os,sys
import tkinter as tk
import ttkbootstrap as ttk
from threading import Thread
from LogSystem import Log
from ttkbootstrap.constants import *
from ColorChange import animationObj
from ExternalCommunication import SerialClass

class CarUI:

    def __init__(self):
        self.Restart=0
        self.Close=False
        self.Triggle=False
        self.Log=Log()
        try:
            print(self.Restarted)
        except:
            pass
        self.MainUI()

    #Define which port need to link
    def Communication(self):
        try:
            if self.Triggle:
                self.Port=self.Log.MainInitalize()["Port"]
            else:
                self.Port = self.Combox.get()
            self.SerialLink = serial.Serial(self.Port, 9600, timeout=10)
            self.Community=SerialClass(self.SerialLink)
            self.TransToDashboardTreads()
        except Exception as err:
            Thread(target=self.MessageBoxThread,args=("Connect Error",err)).start()

    #Define the start interface, used to link communication port
    def MainUI(self):
        self.root = tk.Tk()
        ttk.Style("minty")
        self.root.overrideredirect(True)
        self.ScreenWidth, self.ScreenHeight = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.ScreenWidthMiddle, self.ScreenHeightMidddle = self.ScreenWidth//2, self.ScreenHeight//2
        #root.geometry(f"{ScreenWidth}x{ScreenHeight}")

        self.BackgroundCanvas = ttk.Canvas(
            self.root, width=self.ScreenWidth, height=self.ScreenHeight)
        self.BackgroundCanvas = ttk.Canvas(
            self.root, width=self.ScreenWidth, height=self.ScreenHeight)
        self.StartButton = ttk.Button(
            self.root, text="Start!", command=self.Communication)
        self.Combox = ttk.Combobox(self.root, textvariable="COM PORT")
        self.Combox.set("/dev/ttyACM0")
        self.Combox["value"] = ("/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3",
                           "/dev/ttyACM4", "/dev/ttyACM5", "/dev/ttyACM6", "/dev/ttyACM7", "/dev/ttyACM8")

        self.BackgroundCanvas.create_rectangle(
            0, 0, self.ScreenWidth, self.ScreenHeight, fill="#4a4a4a", outline="")
        self.LabelLink = self.BackgroundCanvas.create_text(self.ScreenWidthMiddle-self.ScreenWidthMiddle//50, self.ScreenHeight //
                                    75, text="Please choose the serial port", font=("", self.ScreenHeight//40), fill="#E1DBFF")

        for _ in range(4):
            Thread(target=self.CanvasCircle).start()


        self.Combox.place(x=self.ScreenWidthMiddle-self.ScreenWidthMiddle //22, y=self.ScreenHeight//25)
        self.StartButton.place(x=self.ScreenWidthMiddle-self.ScreenWidthMiddle //50, y=self.ScreenHeight//12)
        self.BackgroundCanvas.pack()

        if self.Log.MainInitalize()["Status"] == "1":
            self.Triggle=True
            self.root.after_idle(self.Communication)

        self.root.mainloop()


    
    def Dashboard(self):
        try:
            KmLabelLeft = self.BackgroundCanvas.create_text(-self.ScreenWidth//30, self.ScreenHeight //
                                                3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
            KmLabelRight = self.BackgroundCanvas.create_text(
                self.ScreenWidth*1.1, self.ScreenHeight//3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
            self.SpeedLeft = self.BackgroundCanvas.create_text(self.ScreenWidth//7, -self.ScreenHeight//4, text="0", font=("", self.ScreenHeight//8), fill="#EDA69F")
            self.SpeedRight = self.BackgroundCanvas.create_text(self.ScreenWidth-self.ScreenWidth//5, -self.ScreenHeight //4, text="0", font=("", self.ScreenHeight//8), fill="#EDA69F")

            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(KmLabelLeft, i/4500, 0)
            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(KmLabelRight, -i/3200, 0)
            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(self.SpeedLeft,0,i/5000)
            for i in range(self.ScreenWidth, 0, -1):
                self.BackgroundCanvas.move(self.SpeedRight,0,i/5000)

            RestartButton=ttk.Button(self.root,text="Restart",width=self.ScreenWidth//105,style=INFO,command=self.RestartMain).place(x=self.ScreenWidth//5,y=self.ScreenHeight//50)
            CloseButton=ttk.Button(self.root,text="Exit",width=self.ScreenWidth//105,style=INFO,command=self.ExitMain,).place(x=self.ScreenWidth-self.ScreenWidth//4,y=self.ScreenHeight//50)
            while True:
                reading=self.Community.readBinary()
                if reading != None:
                    ReadList=reading
                time.sleep(1)
                self.BackgroundCanvas.delete(KmLabelLeft)            
                self.BackgroundCanvas.delete(KmLabelRight)
                self.BackgroundCanvas.delete(self.SpeedLeft)
                self.BackgroundCanvas.delete(self.SpeedRight)
                KmLabelLeft = self.BackgroundCanvas.create_text(self.ScreenWidth//4, self.ScreenHeight//3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
                KmLabelRight = self.BackgroundCanvas.create_text(self.ScreenWidth-self.ScreenWidth//3.35, self.ScreenHeight//3, text="KM/H", font=("", self.ScreenHeight//30), fill="#E3BCD3")
                self.SpeedLeft = self.BackgroundCanvas.create_text(self.ScreenWidth//7, self.ScreenHeight//5, text=ReadList[
                                                    "SpeedLeft"], font=("", self.ScreenHeight//8), fill="#EDA69F")
                self.SpeedRight = self.BackgroundCanvas.create_text(self.ScreenWidth-self.ScreenWidth//5, self.ScreenHeight//5, text=ReadList[
                                                        "SpeedRight"], font=("", self.ScreenHeight//8), fill="#EDA69F")
        except Exception as err:
            Thread(target=self.MessageBoxThread,args=("Dashboard Error",err)).start()


    def TopLineAnimation(self,status,bgcolor="#4A4A4A"):
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

    def MessageBoxThread(self,Title="Not Defined Error",Text="An Error Has Been Occurented"):
        try:
            x1,y1,x2,y2=self.ScreenWidth*1.3-self.ScreenWidth//5,self.ScreenHeight-self.ScreenHeight//4,self.ScreenWidth*1.3-self.ScreenWidth//60,self.ScreenHeight-self.ScreenHeight//15
            r=25
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            self.MessageFrame=self.BackgroundCanvas.create_polygon(points,smooth=True,outline="",fill="#FFFFFF")
            self.MessageTitle=self.BackgroundCanvas.create_text(self.ScreenWidth*1.2,self.ScreenHeight-self.ScreenHeight//4.4,text=Title,font=("",self.ScreenHeight//75),width=self.ScreenWidth//6,fill="#757575")
            self.MessageText=self.BackgroundCanvas.create_text(self.ScreenWidth*1.2,self.ScreenHeight-self.ScreenHeight//7,text=Text,font=("",self.ScreenHeight//85),width=self.ScreenWidth//6,fill="#212121")
            self.Log.BuildLog(Title,Text)
            Thread(target=self.MessageBoxAnimation).start()
        except Exception as err:
            print(err)

    def MessageBoxAnimation(self):
        for i in range(self.ScreenWidth//7,0,-1):
            self.BackgroundCanvas.move(self.MessageFrame,-i/87,0)
            self.BackgroundCanvas.move(self.MessageTitle,-i/85, 0)
            self.BackgroundCanvas.move(self.MessageText,-i/85, 0)
        time.sleep(2)
        for i in range(0,self.ScreenWidth//7):
            self.BackgroundCanvas.move(self.MessageFrame,i/87,0)
            self.BackgroundCanvas.move(self.MessageTitle,i/85, 0)
            self.BackgroundCanvas.move(self.MessageText,i/85, 0)
        self.BackgroundCanvas.delete(self.MessageFrame,self.MessageTitle,self.MessageText)


    def CanvasCircle(self):
        try:
            while True:
                StartMovementWidth = random.randint(self.ScreenWidth//15, self.ScreenWidth)
                StartMovementHeight = random.randint(self.ScreenHeight//15, self.ScreenHeight)
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
                    self.BackgroundCanvas.move(oval, MoveWidthValue, MoveHeightValue)
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
            Thread(target=self.MessageBoxThread,args=("Transfer to dashboard Error",err)).start()

    def ExitMain(self):
        self.Close = True
        self.RestartMain()


    def RestartMain(self):
        if self.Restart == 0:
            self.FirstTime=time.time()
        self.Restart+=1
        if time.time()-self.FirstTime>2:
            self.Restart=0
        if self.Close:
            Thread(target=self.MessageBoxThread,args=("Restart Warning","To Exit the main program, you need to press the Exit button for 2 times.")).start()
        else:
            Thread(target=self.MessageBoxThread,args=("Restart Warning","To restart the main program, you need to press the restart button for 2 times.")).start()
        if self.Restart==2 :
            self.Restarted=True
            self.SerialLink.close()
            if self.Close:
                self.Log.ChangeInitalizeStatus()
                self.Log.Close()
                os._exit(0)
            else:
                self.Log.ChangeInitalizeStatus(1,self.Port)
                self.Log.Close()
                self.root.destroy()
                os.system(sys.executable+" "+sys.argv[0])
                new=CarUI().Communication()
                new.Communication()

        

CarUI()