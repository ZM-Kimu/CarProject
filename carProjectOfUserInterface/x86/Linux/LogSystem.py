import os
import datetime


class Log:

    def __init__(self) -> None:
        self.File = "MainUILog.txt"
        self.__ReadLog()

    def __ReadLog(self):
        Dir,="None",
        for A,_,C in os.walk(os.getcwd()):
            if self.File in C:
                Dir=A
                break
        if os.path.exists(Dir+"/"+self.File):
            self.Open = open(Dir+"/"+self.File, "rt+")
        else:
            self.Open = open(os.getcwd()+"/"+self.File, "wt+")


    # Status 0 means Exit Normally, 1 means Restart
    def MainInitalize(self):
        self.Open.seek(0, 0)
        Read = self.Open.readline().strip("\n")
        if "Status" in Read and "Port" in Read:
            Status = eval(Read)
        else:
            Status = self.ChangeInitalizeStatus()
        return Status

    def ChangeInitalizeStatus(self, Status=0, Port="COM5"):
        self.Open.seek(0, 0)
        self.Open.write("{"+f'"Status":"{Status}","Port":"{Port}"'+"}\n")
        return {"Status": Status, "Port": Port}

    def BuildLog(self, Title, Text):
        Time = datetime.datetime.now()
        self.Open.seek(0, 2)
        self.Open.write(str(Time)+"\n"+str(Title)+"\n"+str(Text)+"\n")

    def Close(self):
        self.Open.close()
