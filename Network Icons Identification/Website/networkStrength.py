import cv2
import numpy as np
from matplotlib import pyplot as plt

def identify_network_strength(image_dir, coordinates):
    img = cv2.imread(image_dir)[coordinates[0]:coordinates[1], coordinates[2]:coordinates[3]] # crop image
    img2 = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert image to grey scale
    _, img_thresh = cv2.threshold(gray, None, 255, cv2.THRESH_TRIANGLE) # if THRESH_BINARY is used instead, change 2nd parameter to 195
    
    
    # if white background, invert image
    if img_thresh[0][0] == 255:
        img_thresh = cv2.bitwise_not(img_thresh)

    contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # filter contours for contours that are bars
    bar_contours = []

    for contour in contours:
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) < 10: # filter contours that have less than 10 vertices
            x, y, w, h = cv2.boundingRect(approx)
            bar_contours.append((contour, (x, y, w, h)))
        
    # list of average magnitude of each bar
    totalBars = len(bar_contours)
    bar_magnitudes = []

    # mask each bar and get average magnitude of the colours within the mask
    for contour, (x, y, w, h) in bar_contours:
        mask = np.zeros_like(img_thresh)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        
        mean_val = cv2.mean(gray, mask)[0]
        bar_magnitudes.append(mean_val)
    
    
    activeBars = 1
    
    # closenest threshold, (INCREASE TO MAKE MORE SENSITIVE)
    closeness_to_first = 20
    rolling_average = bar_magnitudes[0]
    
    # count number of active bars by comparing magnitude of each bar to the rolling average, which is the average of all the other previous active bars
    
    for i in range(1, len(bar_magnitudes)):
        if abs(bar_magnitudes[i] - rolling_average) < closeness_to_first:
            rolling_average = (rolling_average + bar_magnitudes[i]) / 2
            activeBars += 1
    
    # Save Empty Image
    cv2.imwrite('static/signalStrength.png', img2)
    
    # Save all contours
    cv2.drawContours(img2, [contour for contour, _ in bar_contours], -1, (0, 255, 0), 2)
    cv2.imwrite('static/contours.png', img2)
    
    # print for debug purposes
    print(bar_magnitudes)
    
    return f"{activeBars}/{totalBars}"