
class SerialClass:

    def __init__(self,Link):
        self.ReadPort=Link

    def readBinary(self):
        read=self.ReadPort.readline()
        if read != "\n" and read != "":
            read=eval(read.decode().strip())
            return read