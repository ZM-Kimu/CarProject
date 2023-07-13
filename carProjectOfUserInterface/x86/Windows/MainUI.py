import threading
import serial
import random
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ColorChange import animationObj
from ExternalCommunication import SerialClass as SeC


def LinkPort():
    try:
        global Community
        Port = combox.get()
        serialLink = serial.Serial(Port, 9600, timeout=10)
        Community = SeC(serialLink)
        MainPage()
    except:
        return 0


def readData(Linking):
    global ReadDatas
    print("gotread")


def TopLineAnimation(status, bgcolor="#4A4A4A"):
    if status == "health":
        FillColor = "#8CC9C8"
    if status == "warning":
        FillColor = "#F510CA"
    if status == "emergency":
        FillColor = "#FF0000"
    startPointL = ScreenWidth/2
    startPointR = ScreenWidth/2
    y = 3
    offset = 0
    tick = 0
    change = animationObj(FillColor, bgcolor).gradient()
    while True:
        BackgroundCanvas.delete("line")
        if startPointR < ScreenWidth-ScreenWidth/5:
            line = BackgroundCanvas.create_line(
                startPointL, y, startPointR, y, fill=FillColor, width=3)
        else:
            BackgroundCanvas.delete(line)
            line = BackgroundCanvas.create_line(
                startPointL, y, startPointR, y, fill=change[tick], width=3)
            tick += 1
            if tick >= len(change)-1:
                break
        startPointL -= offset
        startPointR += offset
        offset += 1
        BackgroundCanvas.update()


def CanvasCircle():
    while True:
        StartMovementWidth = random.randint(ScreenWidth//15, ScreenWidth)
        StartMovementHeight = random.randint(ScreenHeight//15, ScreenHeight)
        EndMovementWidth = random.randint(
            ScreenWidth//18, ScreenWidth-ScreenWidth//3)
        EndMovementHeight = random.randint(
            ScreenHeight//18, ScreenHeight-ScreenHeight//3)
        MoveWidthValue = ScreenWidth/8000
        MoveHeightValue = ScreenHeight/8000
        BackgroundCanvas.update()
        IsChange = True
        X1, Y1, X2, Y2 = StartMovementWidth, StartMovementHeight, StartMovementWidth + \
            ScreenWidth//3, StartMovementHeight+ScreenWidth//3
        tick = 0
        oval = BackgroundCanvas.create_oval(
            X1, Y1, X2, Y2, fill="#505061", outline="")
        while True:
            PosistionNow = BackgroundCanvas.coords(oval)
            if PosistionNow[0] <= EndMovementWidth and IsChange:
                MoveWidthValue = -MoveWidthValue
                IsChange = False
            if PosistionNow[1] <= EndMovementWidth and IsChange:
                MoveHeightValue = -MoveHeightValue
                IsChange = False
            if abs(PosistionNow[0] - EndMovementWidth) <= ScreenWidth//7000 or abs(PosistionNow[1] - EndMovementHeight) <= ScreenHeight//7000 or abs(PosistionNow[0]) >= ScreenWidth*1.1 or abs(PosistionNow[1]) >= ScreenHeight*1.1 or tick >= 10000:
                break
            BackgroundCanvas.move(oval, MoveWidthValue, MoveHeightValue)
            BackgroundCanvas.update()
            tick += 1


def StartMainPage():
    global ReadDatas
    KmLabelLeft = BackgroundCanvas.create_text(-ScreenWidth//30, ScreenHeight //
                                         3, text="KM/H", font=("", ScreenHeight//30), fill="#E3BCD3")
    KmLabelRight = BackgroundCanvas.create_text(
        ScreenWidth*1.1, ScreenHeight//3, text="KM/H", font=("", ScreenHeight//30), fill="#E3BCD3")
    SpeedLeft = BackgroundCanvas.create_text(ScreenWidth//7, -ScreenHeight//4, text="0", font=("", ScreenHeight//8), fill="#EDA69F")
    SpeedRight = BackgroundCanvas.create_text(ScreenWidth-ScreenWidth//5, -ScreenHeight //4, text="0", font=("", ScreenHeight//8), fill="#EDA69F")

    for i in range(ScreenWidth, 0, -1):
        BackgroundCanvas.move(KmLabelLeft, i/4500, 0)
    for i in range(ScreenWidth, 0, -1):
        BackgroundCanvas.move(KmLabelRight, -i/3200, 0)
    for i in range(ScreenWidth, 0, -1):
        BackgroundCanvas.move(SpeedLeft,0,i/5000)
    for i in range(ScreenWidth, 0, -1):
        BackgroundCanvas.move(SpeedRight,0,i/5000)
    while True:
        BackgroundCanvas.delete(KmLabelLeft)
        KmLabelLeft = BackgroundCanvas.create_text(ScreenWidth//4, ScreenHeight//3, text="KM/H", font=("", ScreenHeight//30), fill="#E3BCD3")
        BackgroundCanvas.delete(KmLabelRight)
        KmLabelRight = BackgroundCanvas.create_text(ScreenWidth-ScreenWidth//3.35, ScreenHeight//3, text="KM/H", font=("", ScreenHeight//30), fill="#E3BCD3")
        BackgroundCanvas.delete(SpeedLeft)
        SpeedLeft = BackgroundCanvas.create_text(ScreenWidth//7, ScreenHeight//5, text=Community.readBinary()[
                                                "Speed"], font=("", ScreenHeight//8), fill="#EDA69F")
        BackgroundCanvas.delete(SpeedRight)
        SpeedRight = BackgroundCanvas.create_text(ScreenWidth-ScreenWidth//5, ScreenHeight//5, text=Community.readBinary()[
                                                "Speed"], font=("", ScreenHeight//8), fill="#EDA69F")


def ForgetFirstPage():
    print("gotForget")
    StartButton.place_forget()
    combox.place_forget()
    for i in range(0, ScreenHeight):
        BackgroundCanvas.move(label, 0, -i/10000)
    BackgroundCanvas.delete(label)


def MainPage():
    threading.Thread(target=LinkPort).start()
    threading.Thread(target=StartMainPage).start()
    threading.Thread(target=ForgetFirstPage).start()
    threading.Thread(target=TopLineAnimation, args=("health",)).start()
    threading.Thread(target=readData(Community)).start()

root = tk.Tk()
# root.overrideredirect(True)
ScreenWidth, ScreenHeight = root.winfo_screenwidth(), root.winfo_screenheight()
ScreenWidthMiddle, ScreenHeightMidddle = ScreenWidth//2, ScreenHeight//2
# root.geometry(f"{ScreenWidth}x{ScreenHeight}")

BackgroundCanvas = ttk.Canvas(root, width=ScreenWidth, height=ScreenHeight)
BackgroundCanvas = ttk.Canvas(root, width=ScreenWidth, height=ScreenHeight)
StartButton = ttk.Button(root, text="Start!", command=LinkPort)
combox = ttk.Combobox(root, textvariable="COM PORT")
combox.set("COM5")
combox["value"] = ("COM1", "COM2", "COM3", "COM4", "COM5",
                   "COM6", "COM7", "COM8", "COM9",)

BackgroundCanvas.create_rectangle(
    0, 0, ScreenWidth, ScreenHeight, fill="#4a4a4a", outline="")
label = BackgroundCanvas.create_text(ScreenWidthMiddle-ScreenWidthMiddle//50, ScreenHeight //
                               75, text="Please choose the serial port", font=("", ScreenHeight//40), fill="#E1DBFF")

BackgroundCanvas.update()
threading.Thread(target=CanvasCircle).start()
threading.Thread(target=CanvasCircle).start()
threading.Thread(target=CanvasCircle).start()
threading.Thread(target=CanvasCircle).start()


combox.place(x=ScreenWidthMiddle-ScreenWidthMiddle //
             22, y=ScreenHeight//25)
StartButton.place(x=ScreenWidthMiddle-ScreenWidthMiddle //
                  50, y=ScreenHeight//12)
BackgroundCanvas.pack()



root.mainloop()
