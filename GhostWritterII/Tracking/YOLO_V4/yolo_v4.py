import cv2
import time
import os


def yolo_v4(camera, draw):

    file_dir = os.path.dirname(os.path.realpath('__file__'))
    model = os.path.join(file_dir, 'Tracking\\YOLO_V4\\YOLO_v4_training_last.weights')
    model_configuration = os.path.join(file_dir, 'Tracking\\YOLO_V4\\YOLO_v4-tiny.cfg')
    net = cv2.dnn.readNet(model, model_configuration)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    cap = cv2.VideoCapture(camera)
    _, frame = cap.read()
    height, width, _ = frame.shape

    screen = draw.screen(height, width)

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0

    prv_x = 0
    prv_y = 0
    first_point = 0
    while True:
        _, frame = cap.read()
        frame_id += 1
        height, width, _ = frame.shape

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
                if confidence > 0.5:
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
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                if first_point == 0:
                    prv_x = x
                    prv_y = y
                    first_point = first_point + 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                draw.draw_pencil(screen, prv_x, prv_y, x, y, (255, 255, 0), 2)
                prv_x = x
                prv_y = y
                cv2.putText(frame, "pencil" + " " + str(round(confidence, 2)), (x, y + 30), font, 3, (255, 255, 255), 3)
                key2 = cv2.waitKey(1)
                if key2 == ord('c'):
                    screen = draw.clear(height, width)
        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv2.imshow("Image", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break


    cap.release()
    cv2.destroyAllWindows()
