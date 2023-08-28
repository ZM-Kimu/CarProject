import time
from LogSystem import Log


class SerialClass:

    def __init__(self, Link):
        self.ReadPort = Link
        self.Log = Log()

    def readBinary(self):
        try:
            self.ReadPort.reset_input_buffer()
            self.ReadPort.reset_output_buffer()
            read = self.ProtocalReceive()
            LeftBrace = read.index("{")
            RightBrace = read.index("}")
            read = read[LeftBrace:RightBrace+1]
            if read != "\n" and read != "":
                read = eval(read.strip())
                return read
        except Exception as err:
            self.Log.BuildLog("Communication Read", err)

    def ProtocalReceive(self):
        Start = b'\x01'  # 开头标识
        End = b'\x02'    # 尾部标识
        IsStart = False
        Binary = b""
        MessageSize = 0
        Decode = ""
        while True:
            read = self.ReadPort.read()
            if read == Start:
                IsStart = True
            elif read == End:
                IsStart = False
                if len(Binary)-1 == MessageSize:
                    Decode = Binary.decode()
                    break
            else:
                if IsStart:
                    if len(Binary) > 150:
                        break
                    Binary += read
                    MessageSize = int.from_bytes(read, "little")
        return Decode

    def ProtocalSend(self, **args):
        try:
            Start = b'\x03'  # 开头标识
            End = b'\x04'    # 尾部标识
            Message = str(args["args"]["args"])
            MessageSize = len(Message.encode())
            Content = Start + Message.encode() + End + str(MessageSize).encode()
            print(Content)
            self.ReadPort.write(Content)
        except Exception as err:
            self.Log.BuildLog("Communication Send", err)


class SignalSystem:
    def __init__(self, Link):
        self.SerialConnection = Link
        self.SignalCode = -1
        self.CommandSendTime = 999
        self.CommandIsSended = False

    def SignalFormatSending(self, code, **args):
        self.SignalCode = code
        self.CommandSendTime = time.time()
        self.CommandIsSended = True
        SerialClass(self.SerialConnection).ProtocalSend(args=args)

    def CodeSignal(self, Code=str, args=(0, 0, 0)):
        if Code == "-1":
            self.Init()
        elif Code == "00":
            self.EmergencyStop()
        elif Code == "01":
            self.OnEmergencyLightSignal()
        elif Code == "02":
            self.OffEmergencyLightSignal()
        elif Code == "10":
            self.TurnLeftSignal()
        elif Code == "11":
            self.TurnRightSignal()
        elif Code == "12":
            self.BreakSignal()
        elif Code == "50":
            self.LightOff()
        elif Code == "51":
            self.LightRandomGradient()
        elif Code == "52":
            self.LightAudioVisualization()
        elif Code == "53":
            self.LightCustomization(args=args)

    def Init(self):
        self.SignalFormatSending("-1", args={'InitAll': 'True'})

    def EmergencyStop(self):  # 00
        self.SignalFormatSending("00", args={'EmergencyStop': 'True'})

    def OnEmergencyLightSignal(self):  # 01
        self.SignalFormatSending("01", args={'Emergency': 'On'})

    def OffEmergencyLightSignal(self):  # 02/-1
        self.SignalFormatSending("-1", args={'Emergency': 'Off'})

    def TurnLeftSignal(self):  # 10
        self.SignalFormatSending("10", args={'Turnning': 'Left'})

    def TurnRightSignal(self):  # 11
        self.SignalFormatSending("11", args={'Turnning': 'Right'})

    def BreakSignal(self):  # 12
        self.SignalFormatSending("12", args={'Break': 'True'})

    def LightOff(self):  # 50/-1
        self.SignalFormatSending("-1", args={'LightMode': 'Off'})

    def LightRandomGradient(self):  # 51
        self.SignalFormatSending("51", args={'LightMode': 'Gradient'})

    def LightAudioVisualization(self):  # 52
        self.SignalFormatSending("52", args={'LightMode': 'ByAudio'})

    def LightCustomization(self, args=(0, 0, 0)):  # 53
        self.SignalFormatSending("53", args={'LightMode': f'{args}'})

    def AutoEmergencyLight(self):
        if self.SignalCode == "01":
            self.OffEmergencyLightSignal()
        elif self.SignalCode:
            self.OnEmergencyLightSignal()
            
