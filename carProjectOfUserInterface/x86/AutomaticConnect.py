import serial
from time import sleep
from ExternalFileController import Language,Config


class AutoCheck:

    def __init__(self):
        self.proccess=""
        self.bandRate = (9600, 19200, 115200)
        self.result=0
        self.lang=Language(Config().language).lang

    def start(self,OS):
        if OS == "Windows":
            self.result=self.windowsShooting()
        elif OS == "Linux":
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
                self.proccess=f"{self.lang['Connect.Auto.Detail.Port']} {com}"
                try:
                    conSerial = serial.Serial(f"COM{com}")
                    for bR in self.bandRate:
                        conSerial.close()
                        conSerial = serial.Serial(f"COM{com}", bR)
                        sleep(4)
                        if self.serialCheck(conSerial)["Status"] == 1:
                            self.proccess=f"{self.lang['Connect.Auto.Found.Port']} {com}, {self.lang['Connect.Auto.Found.Bandrate']} {bR}"
                            return f"COM{com}", bR
                except:
                    pass
        except:
            pass
        self.result=None


    def linuxShooting(self):
        try:
            for acm in range(11):
                self.proccess=f"Proccess in port {acm}"
                try:
                    conSerial = serial.Serial(f"/dev/ttyACM{acm}")
                    for bR in self.bandRate:
                        conSerial.close()
                        conSerial = serial.Serial(f"/dev/ttyACM{acm}", bR)
                        sleep(4)
                        if self.serialCheck(conSerial)["Status"] == 1:
                            self.proccess=f"Find device in {acm}, bandrate is {bR}"
                            return f"/dev/ttyACM{acm}", bR
                except:
                    pass
        except:
            pass
        self.result=None


