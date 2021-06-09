from .Depth_Camera import Depth_Camera as Dpc
from .IP_Camera import IP_Camera as Ipc
from .Laptop_Camera import Laptop_Camera as Lpc


def camera(camera_type):
    if camera_type == "Depth":
        return Dpc
    elif camera_type == "IP":
        return Ipc
    elif camera_type == "Laptop":
        return Lpc

