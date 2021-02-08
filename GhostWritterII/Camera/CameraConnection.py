from Camera.Depth_Camera import Depth_Camera as Dpc
from Camera.IP_Camera import IP_Camera as Ipc
from Camera.Laptop_Camera import Laptop_Camera as Lpc


def camera(camera_type):
    if camera_type == "Depth":
        return Dpc.depth_camera()
    elif camera_type == 0:
        return Lpc.lab_camera()
    else:
        return Ipc.ip_camera(camera_type)
