from Tracking import Tracking_Controller as Tc
from Camera import CameraConnection as Cc
from Draw import Draw_Controller as Dr


def get_camera():

    while True:
        camera_number = int(input("Select your camera type\n 1 - Default camera (lapTop camera) \n "
                                  "2 - IP Camera \n 3 - Depth Camera\n"))
        if camera_number == 1:
            cameraValue = 0
            cameraConnection=Cc.camera("Laptop")
            break
        elif camera_number == 2:
            ip = input("Enter your IP Camera: ")  # http://192.168.43.1:8080/video
            cameraValue = ip
            cameraConnection=Cc.camera("IP")
            break
        elif camera_number == 3:
            cameraValue = ""
            cameraConnection=Cc.camera("Depth")
            break
        else:
            print("Invalid Input, Please Enter again correctly\n")
    return cameraConnection,cameraValue


def get_draw_type():
    while True:
        draw_number = int(input("Select Drawing way\n 1 - PyGame \n 2 - Open CV\n"))
        if draw_number == 1:
            draw_ty = 1
            break
        elif draw_number == 2:
            draw_ty = 2
            break
        else:
            print("Invalid Input, Please Enter again correctly\n")
    return Dr.draw_on_window(draw_ty)


def get_model():
    while True:
        model_number = int(input("Select Model type\n 1 - YOLO_V4 \n"))
        if model_number == 1:
            model_type = 1
            break
        # elif model_number == 2:
        #     model_type = 2
        #     break
        # elif model_number == 3:
        #     model_type = 3
        #     break
        else:
            print("Invalid Input, Please Enter again correctly\n")
    return model_type


cameraConnection, cameraValue = get_camera()

Tc.tracking_controller(cameraConnection, cameraValue, get_model(), get_draw_type())
