from Tracking.PencilModel import object_detaction as PM
from Tracking.MarkerModel import object_detaction as MM


def tracking_controller(cameraConnection,cameraValue,model, draw):
    if model == 1:
        PM.tracking_object(cameraConnection,cameraValue,draw)
    elif model == 2:
        MM.tracking_object(cameraConnection,cameraValue,draw)
