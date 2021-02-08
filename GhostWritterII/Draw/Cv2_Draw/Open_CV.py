import numpy as np
import cv2

"""
def click_to_clear(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 50 <= x <= 130:
            if 20 <= y <= 60:
                paint_window = np.zeros((1000, 1000, 3)) + 255
                cv2.rectangle(paint_window, (50, 20), (130, 60), (0, 0, 255), 2)
                cv2.putText(paint_window, "Clear", (57, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.imshow("OpenCV", paint_window)
"""


def clear(height, width):
    paint_window = np.zeros((height, width, 3)) + 255
    cv2.imshow("OpenCV", paint_window)

    return paint_window


def screen(height, width):
    paint_window = np.zeros((height, width, 3)) + 255
    # cv2.rectangle(paint_window, (50, 20), (130, 60), (0, 0, 255), 2)
    # cv2.putText(paint_window, "Clear", (57, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow("OpenCV", paint_window)
    return paint_window


def draw_pencil(paint_window, xp, yp, x, y, color_of_drawing, thickness):

    cv2.line(paint_window, (xp, yp), (x, y), color_of_drawing, thickness)
    cv2.imshow("OpenCV", paint_window)
    # cv2.setMouseCallback('image', click_to_clear)
