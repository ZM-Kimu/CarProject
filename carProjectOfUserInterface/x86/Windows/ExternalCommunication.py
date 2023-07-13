
class SerialClass:

    def __init__(self, Link):
        self.ReadPort = Link

    def readBinary(self):
        read=self.ProtocalReceive()
        LeftBrace=read.index("{")
        RightBrace=read.index("}")
        read=read[LeftBrace:RightBrace+1]
        if read != "\n" and read != "":
            read = eval(read.strip())
            return read

    def ProtocalReceive(self):
        Start = b'\x01'  # 开头标识
        End = b'\x02'    # 尾部标识
        IsStart = False
        Binary = b""
        MessageSize = 0

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
                    Binary += read
                    MessageSize = int.from_bytes(read, "little")
        return Decode

    def ProtocalSend(self,Message):
        Start = b'\x03'  # 开头标识
        End = b'\x04'    # 尾部标识
        MessageSize=len(Message.encode())
        Content=Start + Message.encode() + End + bytes([MessageSize])
        self.ReadPort.write(Content)
        
