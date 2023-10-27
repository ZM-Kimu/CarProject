import pygame
import ctypes
from time import sleep
from pygame import joystick


pygame.init()
Joy = joystick.Joystick(0)
Joy.init()


class xInputVibration(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]


def vibration(controller, left_motor, right_motor):
    XInputSetState = ctypes.windll.xinput1_1.XInputSetState
    XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(xInputVibration)]
    XInputSetState.restype = ctypes.c_uint
    vibration = xInputVibration(
        int(left_motor * 65535), int(right_motor * 65535))
    XInputSetState(controller, ctypes.byref(vibration))

#检查手柄的动作
while True:
    pygame.event.get()
    axis = []
    button = []
    hat = []

    for i in range(Joy.get_numaxes()):
        axis.append(round(Joy.get_axis(i), 2))
    for i in range(Joy.get_numbuttons()):
        button.append(Joy.get_button(i))
    for i in range(Joy.get_numhats()):
        hat.append(Joy.get_hat(i))
    #if axis[2] == 1 or axis[2] == -1:
    #    vibration(0, 1, 1)
    #else:
    #    vibration(0, 0, 0)
    print(axis, button, hat)
    # sleep(0.1)
