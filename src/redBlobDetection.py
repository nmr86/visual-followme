import cv2

import numpy as np


def detect_target(hist, frame):
    prob = filter_red_pixels(hist, frame)
    binary_img = clean_up_with_morphology(prob)
    target = detect_biggest_polygon(binary_img)
    return target

def filter_red_pixels(hist, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    unsaturated_pixels = discard_saturated_pixels(hsv)  
    red_pixels = filter_by_color(hist, hsv)
    red_pixels &= unsaturated_pixels
    return red_pixels

def discard_saturated_pixels(hsv):
    mask = cv2.inRange(hsv, np.array((0., 150., 0.)), np.array((180., 255., 255.)))
    return mask

def filter_by_color(hist, hsv):
    prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
    return prob

def clean_up_with_morphology(prob):
    erode = cv2.erode(prob, None, iterations=1)
    dilated = cv2.dilate(erode, None, iterations=2)
    binary_img = cv2.erode(dilated, None, iterations=1)
    return binary_img

def detect_biggest_polygon(binary_img):
    binary_img_to_process = binary_img.copy()  # contour detection will mess up the image
    contours, hierarchy = cv2.findContours(binary_img_to_process, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = None
    if contours != []:
        biggest_contour_index = 0
        for i in range(1, len(contours)):
            if cv2.contourArea(contours[i]) > cv2.contourArea(contours[biggest_contour_index]):
                biggest_contour_index = i
        
        biggest_contour = contours[biggest_contour_index]
    return biggest_contour
