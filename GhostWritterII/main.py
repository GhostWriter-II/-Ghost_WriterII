# from Tracking import Tracking_Controller as Tc
# from Camera import CameraConnection as Cc
# from Draw import Draw_Controller as Dr
#
#
# def get_camera():
#
#     while True:
#         camera_number = int(input("Select your camera type\n 1 - Default camera (lapTop camera) \n "
#                                   "2 - IP Camera \n 3 - Depth Camera\n"))
#         if camera_number == 1:
#             cameraValue = 0
#             cameraConnection=Cc.camera("Laptop")
#             break
#         elif camera_number == 2:
#             ip = input("Enter your IP Camera: ")  # http://192.168.43.1:8080/video
#             cameraValue = ip
#             cameraConnection=Cc.camera("IP")
#             break
#         elif camera_number == 3:
#             cameraValue = ""
#             cameraConnection=Cc.camera("Depth")
#             break
#         else:
#             print("Invalid Input, Please Enter again correctly\n")
#     return cameraConnection,cameraValue
#
#
# def get_draw_type():
#     while True:
#         draw_number = int(input("Select Drawing way\n 1 - PyGame \n 2 - Open CV\n"))
#         if draw_number == 1:
#             draw_ty = 1
#             break
#         elif draw_number == 2:
#             draw_ty = 2
#             break
#         else:
#             print("Invalid Input, Please Enter again correctly\n")
#     return Dr.draw_on_window(draw_ty)
#
#
# def get_model():
#     while True:
#         model_number = int(input("Select Model type\n 1 - pencil object \n 2 - marker object \n"))
#         if model_number == 1:
#             model_type = 'pencil'
#             break
#         elif model_number == 2:
#             model_type = 'marker'
#             break
#         else:
#             print("Invalid Input, Please Enter again correctly\n")
#     return model_type
#
# data={}
#
# cameraConnection, cameraValue = get_camera()
# model=get_model()
# draw=get_draw_type()
# data['cameraConnection']=cameraConnection
# data['cameraValue']=cameraValue
# data['model']=model
# data['draw']=draw
# data['thickness']=2
# data['lineColor']=(255, 0, 0)
# Tc.tracking_controller(data)
from GUI import UI as ui

ui.UI()