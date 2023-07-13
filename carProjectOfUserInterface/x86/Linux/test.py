import os 
for A,B,C in os.walk(os.getcwd()):
    if "MainUILog" in C:
        if os.exists(A+"/"+C):
            self.Open = open(A+"/"+C, "wt+")
