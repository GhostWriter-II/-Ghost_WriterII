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

def tracking_object(cameraConnection,cameraValue,draw):

    file_dir = os.path.dirname(os.path.realpath('__file__'))
    model = os.path.join(file_dir, 'Tracking\\YOLO_V4\\YOLO_v4_training_last2.weights')
    model_configuration = os.path.join(file_dir, 'Tracking\\YOLO_V4\\YOLO_v4-tiny.cfg')
    net = cv2.dnn.readNet(model, model_configuration)

    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

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
    while True:
        frame,depth_frame = cameraConnection.get_frame(camera)
        frame = cv2.resize(frame, (640, 480))
        #frame=cv2.flip(frame,1)
        #depth_frame=cv2.flip(depth_frame,1)
        frame_id += 1
        #height, width, _ = frame.shape

        confidences, boxes, indexes =object_detaction(net,output_layers,frame,width,height)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                if cameraValue=="":
                    point = (x-20, y)
                    z=depth_frame[point[1],point[0]]-250
                    #z = 100000
                    # for wi in range(w):
                    #     for he in range(h):
                    #         t=depth_frame[y+wi, x+he]-250
                    #         if 0<t<z :
                    #             z=t
                    z=int(z*2.5)
                    print("X: " + str(x))
                    print("Y: " + str(y))
                    print("z: " + str(z))
                    cv2.circle(depth_frame, point, 5, (255, 255, 255), 4)
                    cv2.circle(frame, point, 5, (0, 0, 255), 4)
                    if first_point == 0:
                        prv_x = x
                        prv_z=z
                        first_point = first_point + 1

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.putText(frame, "pencil" + " " + str(round(confidence, 2)), (x, y + 70), font, 3, (255, 255, 255), 2)
                    if y<miny:
                        prv_x=0
                        prv_z=0
                        first_point=0
                    elif y >= miny and (maxz>z>0 and maxz>prv_z >0):
                        draw.draw_line(screen, width-prv_x, prv_z, width-x, z, (0, 255, 0), 2)
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
                    draw.draw_line(screen, prv_x, prv_y,x, y, (0, 255, 0), 2)
                    prv_x = x
                    prv_y = y

        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv2.imshow("Image",frame)
        if cameraValue=="":
            cv2.imshow("Depth", depth_frame*255)
        key = cv2.waitKey(1)
        if key& 0xFF == ord('c') or key& 0xFF == ord('C'):
            screen = draw.clear(height, width)
            print("clear")
        if key& 0xFF == ord('q') or key& 0xFF == ord('Q'):
            print("quit")
            break
    cameraConnection.release(camera)
    cv2.destroyAllWindows()
