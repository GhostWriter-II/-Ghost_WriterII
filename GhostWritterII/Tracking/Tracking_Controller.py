from Tracking.YOLO_V4 import yolo_v4 as yolo4


def tracking_controller(cameraConnection,cameraValue,model, draw):
    if model == 1:
        yolo4.tracking_object(cameraConnection,cameraValue,draw)
