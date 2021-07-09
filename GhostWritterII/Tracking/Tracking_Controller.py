

def tracking_controller(data):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    if data['model'] == "pencil":
        model = os.path.join(file_dir, 'Tracking\\PencilModel\\YOLO_v4_training_last.weights')
        model_configuration = os.path.join(file_dir, 'Tracking\\PencilModel\\YOLO_v4-tiny.cfg')
        data['modelFilePath']=model
        data['modelConfigurationPath']=model_configuration
        tracking_object(data)
    elif data['model'] == "marker":
        model = os.path.join(file_dir, 'Tracking\\MarkerModel\\YOLO_v4_training_last.weights')
        model_configuration = os.path.join(file_dir, 'Tracking\\MarkerModel\\YOLO_v4-tiny.cfg')
        data['modelFilePath']=model
        data['modelConfigurationPath']=model_configuration
        tracking_object(data)

import cv2
import time
import os
def object_detaction(net,output_layers,frame,width,height):
    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            confidence = scores[0]
            if confidence > 0.7:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
    return confidences,boxes,indexes

def tracking_object(data):

    modelpath=data['modelFilePath']
    configurationPath=data['modelConfigurationPath']
    cameraConnection=data['cameraConnection']
    cameraValue=data['cameraValue']
    draw=data['draw']
    font_scale=data['font']
    lineColor=data['lineColor']
    thickness=data['thickness']
    model=data['model']
    net = cv2.dnn.readNet(modelpath,configurationPath )

    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    camera = cameraConnection.cameraInit(cameraValue)
    frame,depth_frame = cameraConnection.get_frame(camera)
    frame = cv2.resize(frame, (640, 480))
    height, width, _ = frame.shape
    screen = draw.screen(height, width)

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0

    prv_x = 0
    prv_z = 0
    prv_y = 0
    first_point = 0
    miny=200
    maxz=500
    minz=250
    imageNum=1
    depthPoint=20
    if model=="marker":
        depthPoint=10
    while True:
        frame,depth_frame = cameraConnection.get_frame(camera)
        frame = cv2.resize(frame, (640, 480))
        #frame=cv2.flip(frame,1)
        #depth_frame=cv2.flip(depth_frame,1)
        frame_id += 1
        #height, width, _ = frame.shape
        key = cv2.waitKey(1)
        if key& 0xFF == ord('c') or key& 0xFF == ord('C'):
            screen = draw.clear(height, width)
            print("clear")
        if key& 0xFF == ord('q') or key& 0xFF == ord('Q'):
            print("quit")
            break
        if key& 0xFF == ord('s') or key& 0xFF == ord('S'):
            draw.save_as_image(screen,imageNum)
            imageNum+=1
            print("save")

        confidences, boxes, indexes =object_detaction(net,output_layers,frame,width,height)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                if cameraValue=="":
                    if key & 0xFF == ord('e') or key & 0xFF == ord('E'):
                        miny=y-10
                        print("set snapshot")
                    point = (x-depthPoint, y)
                    z=depth_frame[point[1],point[0]]-minz
                    #z = 100000
                    # for wi in range(w):
                    #     for he in range(h):
                    #         t=depth_frame[y+wi, x+he]-250
                    #         if 0<t<z :
                    #             z=t
                    z=int(z*font_scale)

                    cv2.circle(depth_frame, point, 5, (255, 255, 255), 4)
                    cv2.circle(frame, (x,miny), 5, (0, 0, 255), 4)
                    cv2.circle(frame, (x, y), 5, (255, 0, 0), 4)

                    if first_point == 0:
                        prv_x = x
                        prv_z=z
                        first_point = first_point + 1

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.putText(frame, model + " " + str(round(confidence, 2)), (x, y + 70), font, 3, (255, 255, 255), 2)
                    if y<miny:
                        prv_x=0
                        prv_z=0
                        first_point=0
                    elif y >= miny and (maxz>z>0 and maxz>prv_z >0):
                        print("X: " + str(x))
                        print("Y: " + str(y))
                        print("z: " + str(z))
                        draw.draw_line(screen, width-prv_x, prv_z, width-x, z, lineColor,thickness)
                        prv_x = x
                        prv_z = z
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.putText(frame, "pencil" + " " + str(round(confidence, 2)), (x, y + 70), font, 3,
                                (255, 255, 255), 2)
                    if first_point == 0:
                        prv_x =x
                        prv_y=y
                        first_point = first_point + 1
                    draw.draw_line(screen, prv_x, prv_y,x, y, lineColor,thickness)
                    prv_x = x
                    prv_y = y

        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv2.imshow("Image",frame)
        if cameraValue=="":
            cv2.imshow("Depth", depth_frame*255)

    cameraConnection.release(camera)
    cv2.destroyAllWindows()
