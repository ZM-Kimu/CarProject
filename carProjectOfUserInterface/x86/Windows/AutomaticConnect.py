import platform
import serial
from time import sleep


class AutoCheck:

    def __init__(self):
        platformNow = platform.system()
        self.bandRate = (9600, 19200, 115200)
        if platformNow == "Windows":
            self.result=self.windowsShooting()
        elif platformNow == "Linux":
            self.result=self.linuxShooting()

    def serialCheck(self,link):
        read = link.read_all()
        if b"Status" in read and b"\x01" in read and b"\x02" in read:
            start = read.index(b"\x01")
            end = read.index(b"\x02")
            read=read[start+1:end-1].decode()
            return eval(read)
        return {"Status":0}

    def windowsShooting(self):
        try:
            for com in range(11):
                try:
                    conSerial = serial.Serial(f"COM{com}")
                    for bR in self.bandRate:
                        conSerial.close()
                        conSerial = serial.Serial(f"COM{com}", bR)
                        sleep(4)
                        if self.serialCheck(conSerial)["Status"] == 1:
                            return f"COM{com}", bR
                except:
                    pass
        except:
            pass


    def linuxShooting(self):
        try:
            for acm in range(11):
                try:
                    conSerial = serial.Serial(f"/dev/ttyACM{acm}")
                    for bR in self.bandRate:
                        conSerial.close()
                        conSerial = serial.Serial(f"/dev/ttyACM{acm}", bR)
                        sleep(2)
                        if self.serialCheck(conSerial)["Status"] == 1:
                            return f"/dev/ttyACM{acm}", bR
                except:
                    pass
        except:
            pass


