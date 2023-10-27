import random
import ttkbootstrap as ttk
from time import sleep
from typing import Literal
from threading import Thread
from ttkbootstrap.constants import *


class ColorGradient:

    def __init__(self, colorOri, colorWanna, *args):
        self.Ori = colorOri
        self.middle = args
        self.Wanna = colorWanna
        self.alphaList = "0123456789ABCDEF"
        self.FinalOutputList = []

    def __getColorList(self):
        colorList1, colorList2 = [], []
        for i in self.Ori:
            if i != "#":
                colorList1.append(i)
        for i in self.Wanna:
            if i != "#":
                colorList2.append(i)
        self.colorList1 = colorList1
        self.colorList2 = colorList2

    def __colorCompare(self):
        self.__getColorList()
        is_1_BiggerThan_2 = []
        for i in range(0, 6):
            if self.colorList1[i] > self.colorList2[i]:
                is_1_BiggerThan_2.append(True)
            elif self.colorList1[i] < self.colorList2[i]:
                is_1_BiggerThan_2.append(False)
            else:
                is_1_BiggerThan_2.append(0)
        self.bigger = is_1_BiggerThan_2

    def __loopGet(self):
        self.__colorCompare()
        tickForColor, tickForList = 0, 0
        after = ""
        prefix = "#"
        while True:
            beforeAdd, backAdd = "", ""
            if self.bigger[tickForColor]:
                after = str(
                    self.alphaList[self.alphaList.index(self.colorList1[tickForColor])-1])
            if self.bigger[tickForColor] is False:
                after = str(
                    self.alphaList[self.alphaList.index(self.colorList1[tickForColor])+1])
            elif self.bigger[tickForColor] == 0:
                after = str(self.colorList1[tickForColor])
            tickForColor += 1
            beforeAdd = "".join(self.colorList1[:tickForColor-1])
            backAdd = "".join(self.colorList1[tickForColor:])
            after = prefix+beforeAdd+after+backAdd
            if tickForColor >= 6:
                tickForColor = 0

            self.Ori = after
            self.FinalOutputList.append(self.Ori)
            tickForList += 1
            self.__colorCompare()
            if after == self.Wanna:
                break

    def gradient(self):
        self.__loopGet()
        return self.FinalOutputList

    def basicTransaction(self):
        transactionList = []
        transactionList.append(self.Ori)
        for i in self.middle:
            transactionList.append(i)
        transactionList.append(self.Wanna)
        return transactionList


class StyleType:
    def __init__(self, window, ScreenWidth, ScreenHeight, Canvas):
        self.Window = window
        self.ScreenWidth = ScreenWidth
        self.ScreenHeight = ScreenHeight
        self.Canvas = Canvas

    def Place(self, Widget=object, Side: Literal["left", "right", "top", "bottom", "center"] = str, Distance=float, Vertical=float):
        """
        This method can use to define the position of a widget (Button, Input...).
        Widget: The object create by StyleType.
        Side: The side of widget,include "left","right","top","bottom","center".
        Distance: The distance of anchor side, max is 200.
        Vertical: The distance of vertical with Distance's direction(if Distance is x, then Vertical is y), max is 200.  
        CAUTION: If Anchor is center, then Distance is x and Vertical is y.
        """
        if Side == "left":
            Widget.place(x=Distance/200*self.ScreenWidth,
                         y=self.ScreenHeight // 2+Vertical/200*self.ScreenHeight, anchor="center")
        elif Side == "right":
            Widget.place(x=self.ScreenWidth-Distance/200*self.ScreenWidth,
                         y=self.ScreenHeight//2+Vertical/200*self.ScreenHeight, anchor="center")
        elif Side == "top":
            Widget.place(x=self.ScreenWidth//2+Vertical/200*self.ScreenWidth,
                         y=Distance/200*self.ScreenHeight, anchor="center")
        elif Side == "bottom":
            Widget.place(x=self.ScreenWidth//2+Vertical/200*self.ScreenWidth,
                         y=self.ScreenHeight-Distance/200*self.ScreenHeight, Anchor="center")
        elif Side == "center":
            Widget.place(x=self.ScreenWidth//2+Distance/200*self.ScreenWidth,
                         y=self.ScreenHeight//2+Vertical/200*self.ScreenHeight, Anchor="center")

    def CanvasPosition(self, Side: Literal["left", "right", "top", "bottom", "center"] = str, Distance=float, Vertical=float):
        """
        This method can easily return (x,y) positon values to pack a Canvas widget.
        Side: The side of widget,include "left","right","top","bottom","center".
        Distance: The distance of anchor side, max is 200.
        Vertical: The distance of vertical with Distance's direction(if Distance is x, then Vertical is y), max is 200.  
        CAUTION: If Anchor is center, then Distance is x and Vertical is y.
        """
        x = 0
        y = 0
        if Side == "left":
            x = Distance/200*self.ScreenWidth
            y = self.ScreenHeight // 2+Vertical/200*self.ScreenHeight
        elif Side == "right":
            x = self.ScreenWidth-Distance/200*self.ScreenWidth
            y = self.ScreenHeight//2+Vertical/200*self.ScreenHeight
        elif Side == "top":
            x = self.ScreenWidth//2+Vertical/200*self.ScreenWidth
            y = Distance/200*self.ScreenHeight
        elif Side == "bottom":
            x = self.ScreenWidth//2+Vertical/200*self.ScreenWidth
            y = self.ScreenHeight-Distance/200*self.ScreenHeight
        elif Side == "center":
            x = self.ScreenWidth//2+Distance/200*self.ScreenWidth
            y = self.ScreenHeight//2+Vertical/200*self.ScreenHeight
        return x, y

    def CanvasMove(self, Canvas, MoveX, MoveY):
        self.Canvas.move(Canvas, MoveX/200*self.ScreenWidth,
                         MoveY/200*self.ScreenWidth)


class WidgetModual(StyleType):
    def __init__(self, window, ScreenWidth, ScreenHeight, Canvas):
        super().__init__(window, ScreenWidth, ScreenHeight, Canvas)

    def ButtonTheme(self, Color):
        if Color == "red":
            style = SECONDARY
        elif Color == "blue":
            style = INFO
        elif Color == "green":
            style = SUCCESS
        elif Color == "yellow":
            style = WARNING
        elif Color == "orange":
            style = DANGER
        return style

    def Buttons(self, Text=str, Color: Literal["red", "blue", "green", "yellow", "orange"] = str,  Command=None, ButtonWidth=0, *args):
        """
            Text: The words you want to show.
            Color: The Color of Button, "red","blue","green","yellow" or "orange".
            Command: The function you want to execute.
            ButtonWidth: Length of button, max is 200.
            *args(Side, Distance,Vertical): Place the widget, see Place method manual.
        """
        if ButtonWidth:
            Widget = ttk.Button(self.Window, text=Text, width=self.ScreenWidth //
                                (201-ButtonWidth), style=self.ButtonTheme(Color), command=Command)
        else:
            Widget = ttk.Button(self.Window, text=Text,
                                style=self.ButtonTheme(Color), command=Command)
        if args:
            self.Place(Widget, args[0], args[1], args[2])
        return Widget

    def CanvasText(self, Text=str, Color=str, FontSize=int, Side=str, Distance=float, Vertical=float, Width=5000):
        """
            Text: The words you want to show.
            Color: The Color of Text, hex color code.
            FontSize: Size of text, max is 200.
            Position(Side, Distance,Vertical): Place the text, see Place method manual.
            *Width: Decide when need change new line.
        """
        x, y = self.CanvasPosition(Side, Distance, Vertical)
        Canvas = self.Canvas.create_text(x, y, text=Text, font=(
            "", self.ScreenWidth // (201-FontSize)), fill=Color, anchor="center", width=Width)
        return Canvas


class Widgets(WidgetModual):
    def __init__(self, window, ScreenWidth, ScreenHeight, Canvas):
        super().__init__(window, ScreenWidth, ScreenHeight, Canvas)
        self.StopAnimation = False

    def TopLineAnimation(self, Stauts, BgColor="#4A4A4A"):
        """
        Canvas: The place of line.
        Status: The color of Line, "health","warning","emergency"
        BgColor: The background color, use for gradient.
        """
        if Stauts == "health":
            FillColor = "#8CC9C8"
        elif Stauts == "warning":
            FillColor = "#F510CA"
        elif Stauts == "emergency":
            FillColor = "#FF0000"
        startPointL = self.ScreenWidth/2
        startPointR = self.ScreenWidth/2
        y = 1
        offset = 0
        tick = 0
        change = ColorGradient(FillColor, BgColor).gradient()
        while True:
            self.Canvas.delete("line")
            if startPointR < self.ScreenWidth-self.ScreenWidth/5:
                line = self.Canvas.create_line(
                    startPointL, y, startPointR, y, fill=FillColor, width=4)
            else:
                self.Canvas.delete(line)
                line = self.Canvas.create_line(
                    startPointL, y, startPointR, y, fill=change[tick], width=4)
                tick += 1
                if tick >= len(change)-1:
                    break
            self.Canvas.update()
            startPointL -= offset
            startPointR += offset
            offset += 1

    def FadeInAnime(self, StartColor=str, EndColor=str, Text=str, FontSize=int, Side=str, Distance=int, Vertical=int, FadeSpeed: float = 0, AutoFadeOut: bool = False, StayTime: float = 0):
        """
            Text: The words you want to show.
            StartColor: The Color of Text in grandient start, hex color code.
            EndColor: The Color of Text in gradient end, hex color code.
            FontSize: Size of Text, max is 200.
            Position(Side, Distance,Vertical): Place the text, see Place function manual.
            FadeSpeed: Speed of Gradient, max is 1.
            AutoFadeOut: Automatic fading out.
            StayTime: After fade in, how long need fade out.
        """
        try:
            text = self.CanvasText(
                Text, StartColor, FontSize, Side, Distance, Vertical)
            for i in ColorGradient(StartColor, EndColor).gradient():
                self.Canvas.delete(text)
                text = self.CanvasText(
                    Text, i, FontSize, Side, Distance, Vertical)
                self.Canvas.update()
                sleep(0.1-FadeSpeed*0.1)
            sleep(StayTime)
            if AutoFadeOut:
                self.FadeOutAnime(text, EndColor, StartColor, Text,
                                  FontSize, Side, Distance, Vertical, FadeSpeed)
            return text
        except:
            self.Canvas.delete("text")

    def FadeOutAnime(self, text=object, StartColor=str, EndColor=str, Text=str, FontSize=int, Side=str, Distance=int, Vertical=int, FadeSpeed: float = 0):
        """
            Text: The words you want to show.
            StartColor: The Color of Text in grandient start, hex color code.
            EndColor: The Color of Text in gradient end, hex color code.
            FontSize: Size of Text, max is 200.
            Position(Side, Distance,Vertical): Place the text, see Place function manual.
            FadeSpeed: Speed of Gradient, max is 1.
        """
        try:
            for i in ColorGradient(StartColor, EndColor).gradient():
                self.Canvas.delete(text)
                text = self.CanvasText(
                    Text, i, FontSize, Side, Distance, Vertical)
                self.Canvas.update()
                sleep(0.1-FadeSpeed*0.1)
            self.Canvas.delete(text)
        except:
            self.Canvas.delete("text")

    def BackGroundCircleAnime(self):
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
                self.Canvas.update()
                IsChange = True
                X1, Y1, X2, Y2 = StartMovementWidth, StartMovementHeight, StartMovementWidth + \
                    self.ScreenWidth//3, StartMovementHeight+self.ScreenWidth//3
                tick = 0
                oval = self.Canvas.create_oval(
                    X1, Y1, X2, Y2, fill="#505061", outline="")
                while True:
                    PosistionNow = self.Canvas.coords(oval)
                    if PosistionNow[0] <= EndMovementWidth and IsChange:
                        MoveWidthValue = -MoveWidthValue
                        IsChange = False
                    if PosistionNow[1] <= EndMovementWidth and IsChange:
                        MoveHeightValue = -MoveHeightValue
                        IsChange = False
                    if abs(PosistionNow[0] - EndMovementWidth) <= self.ScreenWidth//7000 or abs(PosistionNow[1] - EndMovementHeight) <= self.ScreenHeight//7000 or abs(PosistionNow[0]) >= self.ScreenWidth*1.1 or abs(PosistionNow[1]) >= self.ScreenHeight*1.1 or tick >= 10000:
                        break
                    self.Canvas.move(
                        oval, MoveWidthValue, MoveHeightValue)
                    self.Canvas.update()
                    tick += 1

        except:
            pass

    def LoadingAnime(self, side):
        """
        ### This method is design to create a loading animation.
        Side: The side of animation,include "top","bottom".
        """
        def ovalAnimation():
            speed = 0
            MaxSpeed = 20
            MinSpeed = 6
            step = 0.75
            RangeOffset = self.ScreenWidth//10
            x, y = self.CanvasPosition(side, self.ScreenHeight//50, 0)
            oval = self.Canvas.create_oval(x-RangeOffset, y, x+self.ScreenWidth //
                                           400-RangeOffset, y+self.ScreenWidth//400, outline="", fill="#FFFFFF")
            while True:
                position = self.Canvas.coords(oval)
                if position[0] <= x-RangeOffset//7:
                    MaxSpeed -= step
                    speed = MaxSpeed
                elif position[0] > x-RangeOffset//7 and position[0] < x+RangeOffset//7:
                    speed = MinSpeed
                elif position[0] > x+RangeOffset//7 and position[0] < x+RangeOffset:
                    speed += step
                else:
                    self.Canvas.delete(oval)
                    self.Canvas.update()
                    break
                self.Canvas.move(oval, speed, 0)
                self.Canvas.update()
                sleep(0.03)
        for _ in range(5):
            Thread(target=ovalAnimation).start()
            sleep(0.15)

    def PopMessageBox(self, Title="Not Defined Error", Text="An Error Has Been Occurented"):
        """
        ### This method is use to create a pop up message box.
        Title: The title of this message.
        Text: The content of this message.
        """
        # def messageAnimation():
        x1, y1, x2, y2 = self.ScreenWidth*1.3-self.ScreenWidth//5, self.ScreenHeight - \
            self.ScreenHeight//4, self.ScreenWidth*1.3 - \
            self.ScreenWidth//60, self.ScreenHeight-self.ScreenHeight//15
        r = 25
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2,
                  y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        MessageFrame = self.Canvas.create_polygon(
            points, smooth=True, outline="", fill="#FFFFFF")
        MessageTitle = self.CanvasText(
            Title, "#757575", 70, "bottom", 45, 140, self.ScreenWidth//6)
        MessageText = self.CanvasText(
            Text, "#212121", 50, "bottom", 30, 140, self.ScreenWidth//6)

        for i in range(self.ScreenWidth//7, 0, -1):
            self.Canvas.move(MessageFrame, -i/87, 0)
            self.Canvas.move(MessageTitle, -i/85, 0)
            self.Canvas.move(MessageText, -i/85, 0)
        sleep(2)
        for i in range(0, self.ScreenWidth//7):
            self.Canvas.move(MessageFrame, i/87, 0)
            self.Canvas.move(MessageTitle, i/85, 0)
            self.Canvas.move(MessageText, i/85, 0)
        self.Canvas.delete(MessageFrame, MessageTitle, MessageText)

    def Movement(self, Widget, Mode: Literal["linear", "nonlinear"] = str, Method: Literal["coordinate", "place"] = str, Start=tuple, Stop=tuple, Speed=float, BezierLine=tuple):
        """
        ### This method can move a widget by linear or nonlinear.
        #### Mode: 
        Options are linear or nonlinear.
        #### Method: 
        Coordinate is move by x,y values. Start and Stop must be (x,y). 

        Place is from one place move to another place, Start and Stop must be (Side, Distance,Vertical).
        #### Start: 
        Start from anywhere. Following Place(Side, Distance,Vertical) a tuple.
        #### Stop: 
        End with anywhere. Following Place(Side, Distance,Vertical) a tuple.
        #### Speed: 
        The speed of animation. Range in 0-2. In place Method, speed defined max speed.
        """
        # TODO: Debug the "coordinate" method
        #TODO: NonLinear: create bezierLine
        self.CanvasPosition()
        step = 5000/Speed

        def CalculateDistance(Start, Stop, Method):
            if Method == "place":
                Start = self.CanvasPosition(Start[0], Start[1], Start[2])
                Stop = self.CanvasPosition(Stop[0], Stop[1], Stop[2])
            movementX = Stop[0] - Start[0]
            movementY = Stop[1] - Start[1]
            return (Stop[0], Stop[1], movementX, movementY)

        def Linear():
            move = CalculateDistance(Start, Stop, Method)
            particularX = move[2]/step
            particularY = move[3]/step
            while True:
                position = self.Canvas.coords(Widget)
                if round(position[0]) == round(move[0]) and round(position[1]) == round(move[1]):
                    break
                self.Canvas.move(Widget, particularX, particularY)
                print(position, move)

        def NonLinear():
            minSpeed = 0
            maxSpeed = Speed
            tick = 0
            step = 2000
            variableSpeed = 0
            isIncrease = True

            move = CalculateDistance(Start, Stop, Method)
            particularX = move[2]/step
            particularY = move[3]/step

            increaseValue = maxSpeed/200

            needX = move[2]/2
            needY = move[3]/2

            while True:
                if isIncrease:
                    if tick == 0:
                        variableSpeed = minSpeed
                    elif variableSpeed >= maxSpeed:
                        isIncrease = False
                    else:
                        variableSpeed += increaseValue
                else:
                    if variableSpeed <= minSpeed:
                        break
                    else:
                        variableSpeed -= increaseValue

                position = self.Canvas.coords(Widget)
                if round(position[0]) == round(move[0]) and round(position[1]) == round(move[1]):
                    break
                self.Canvas.move(Widget, particularX*variableSpeed, particularY*variableSpeed)

                tick += 1

        if Mode == "linear":
            Thread(target=Linear).start()
        elif Mode == "nonlinear":
            Thread(target=NonLinear).start()
