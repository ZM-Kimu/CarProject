from LogSystem import Log

class SerialClass:

    def __init__(self, Link):
        self.ReadPort = Link
        self.Log=Log()

    def readBinary(self):
        try:
            self.ReadPort.reset_input_buffer()
            self.ReadPort.reset_output_buffer()
            read=self.ProtocalReceive()
            LeftBrace=read.index("{")
            RightBrace=read.index("}")
            read=read[LeftBrace:RightBrace+1]
            if read != "\n" and read != "":
                read = eval(read.strip())
                return read
        except Exception as err:
            self.Log.BuildLog("Communication Read",err)

    def ProtocalReceive(self):
        Start = b'\x01'  # 开头标识
        End = b'\x02'    # 尾部标识
        IsStart = False
        Binary = b""
        MessageSize = 0
        Decode=""
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


    def ProtocalSend(self,**args):
        try:
            Start = b'\x03'  # 开头标识
            End = b'\x04'    # 尾部标识
            Message=str(args)
            MessageSize=len(Message.encode())
            Content=Start + Message.encode() + End + str(MessageSize).encode()
            self.ReadPort.write(Content)
        except Exception as err:
            self.Log.BuildLog("Communication Send",err)
            
