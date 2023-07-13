import serial
from time import sleep,time
import datetime
from ExternalCommunication import SerialClass
Message="{'Status':'1','Operation':'Start'}"
ReadPort=serial.Serial("COM5",9600)
sc=SerialClass(ReadPort)
timestart=time()
while True:

    Start = b'\x03'  # 开头标识
    End = b'\x04'    # 尾部标识
    MessageSize=len(Message.encode())
    Content=Start + Message.encode() + End + str(MessageSize).encode()
    timenow=time()
    if float(timenow) - float(timestart) > 10:
        byte=ReadPort.write(Content)
    read=ReadPort.read_all()
    print(read.decode())
    sleep(0.5)
