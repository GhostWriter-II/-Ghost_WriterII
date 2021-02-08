from Tracking.YOLO_V4 import yolo_v4 as yolo4
from Tracking.YOLO_V5 import yolo_v5 as yolo5
from Tracking.Mobilenet import mobilenet as mobile


def tracking_objects(model, camera, draw_type):
    if model == 1:
        yolo4.yolo_v4(camera, draw_type)
    elif model == 2:
        yolo5.yolo_v5(camera, draw_type)
    elif model == 4:
        mobile.mobilenet_test(camera, draw_type)
    else:
        mobile.mobilenet(camera, draw_type)
