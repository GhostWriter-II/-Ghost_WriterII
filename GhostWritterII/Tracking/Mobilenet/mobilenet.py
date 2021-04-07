import tensorflow as tf
import cv2 as cv
import os
# import glob
import time


def tracking_object(camera, draw):
    # Fix Relative path problem
    # Take the model from its destination
    file_dir = os.path.dirname(os.path.realpath('__file__'))  # path which main.py located
    model = os.path.join(file_dir, 'Tracking\\Mobilenet\\40000_iteration_specificPencil_model.pb')  # get the model

    # Read the graph that is equal to model configuration.
    with tf.compat.v1.gfile.FastGFile(model, 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    cap = cv.VideoCapture(camera)
    _, frame = cap.read()
    height, width, _ = frame.shape

    screen = draw.screen(height, width)

    font = cv.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0

    prv_x = 0
    prv_y = 0
    first_point = 0

    while True:
        _, frame = cap.read()
        frame_id += 1
        with tf.compat.v1.Session() as sess:

            # Restore session
            sess.graph.as_default()
            tf.import_graph_def(graph_def, name='')

            # Read and preprocess an image.
            rows = frame.shape[0]
            cols = frame.shape[1]
            inp = cv.resize(frame, (300, 300))
            inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

            # Run the model
            out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                            sess.graph.get_tensor_by_name('detection_scores:0'),
                            sess.graph.get_tensor_by_name('detection_boxes:0'),
                            sess.graph.get_tensor_by_name('detection_classes:0')],
                           feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

            # Visualize detected bounding boxes.
            num_detections = int(out[0][0])
            for i in range(num_detections):
                score = float(out[1][0][i])
                bbox = [float(v) for v in out[2][0][i]]
                if score > 0.3:
                    # print("Entered")
                    x = bbox[1] * cols
                    y = bbox[0] * rows
                    if first_point == 0:
                        prv_x = x
                        prv_y = y
                        first_point = first_point + 1
                    right = bbox[3] * cols
                    bottom = bbox[2] * rows
                    cv.rectangle(frame, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
                    draw.draw_pencil(screen, int(prv_x), int(prv_y), int(x), int(y), (255, 255, 0), 2)
                    prv_x = x
                    prv_y = y
                    cv.putText(frame, "pencil" + " " + str(round(score, 2)), (int(x), int(y) + 30), font, 3,
                               (255, 255, 255), 3)

        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv.imshow('TensorFlow MobileNet-SSD', frame)
        key = cv.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv.destroyAllWindows()


"""
    Pictures Testing
def mobilenet(camera, draw_type):
    # Fix Relative path problem
    # Take the model from its destination
    file_dir = os.path.dirname(os.path.realpath('__file__'))  # path which main.py located
    model = os.path.join(file_dir, 'Tracking\\Mobilenet\\40000_iteration_specificPencil_model.pb')  # get the model

    # Read the graph that is equal to model configuration.
    with tf.compat.v1.gfile.FastGFile(model, 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    # images Path
    image_path = glob.glob("Test Images\\*.jpg")
    print("Number of Images: " + str(len(image_path)))

    # for each image
    for img in image_path:
        with tf.compat.v1.Session() as sess:

            # Restore session
            sess.graph.as_default()
            tf.import_graph_def(graph_def, name='')

            # Read and preprocess an image.
            img = cv.imread(img)
            rows = img.shape[0]
            cols = img.shape[1]
            inp = cv.resize(img, (300, 300))
            inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

            # Run the model
            out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                            sess.graph.get_tensor_by_name('detection_scores:0'),
                            sess.graph.get_tensor_by_name('detection_boxes:0'),
                            sess.graph.get_tensor_by_name('detection_classes:0')],
                           feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

            # Visualize detected bounding boxes.
            num_detections = int(out[0][0])
            for i in range(num_detections):
                score = float(out[1][0][i])
                bbox = [float(v) for v in out[2][0][i]]
                if score > 0.3:
                    # print("Entered")
                    x = bbox[1] * cols
                    y = bbox[0] * rows
                    right = bbox[3] * cols
                    bottom = bbox[2] * rows
                    cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)

        cv.imshow('TensorFlow MobileNet-SSD', img)
        key = cv.waitKey()
        if key == 27:
            break
    cv.destroyAllWindows()
    
"""