import cv2
import pytesseract
import argparse
import numpy as np

# Set up argument parser to recieve image path and coordinates of the crop
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-c", "--coordinates",default=[], nargs='+', type=int, help="coordinates of the crop, format: x1 y1 x2 y2")

args = vars(ap.parse_args())

# Read image path and import image
image_path = args["image"]
image = cv2.imread(image_path)

if image == None:
    print("Image not found")
    exit()

# If coordinates are passed in the arguments, crop the image
if args["coordinates"]:
    coordinates = args["coordinates"]
    image = image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Triangle thresholding to convert to binary image
_, img_thresh = cv2.threshold(gray, None, 255, cv2.THRESH_TRIANGLE)

# Invert the binary image if the background (top-left pixel) is white
if img_thresh[0][0] == 255:
    img_thresh = cv2.bitwise_not(img_thresh)
    
# Find contours in the binary image
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

bar_contours = []

# Iterate over the contours
for contour in contours:
    epsilon = 0.01 * cv2.arcLength(contour, True)  # Calculate epsilon for contour approximation
    approx = cv2.approxPolyDP(contour, epsilon, True)  # Approximate the contour
    
    if len(approx) < 10:  # Check if the contour has less than 10 vertices
        x, y, w, h = cv2.boundingRect(approx)  # Get the bounding rectangle of the contour
        bar_contours.append((contour, (x, y, w, h)))  # Add the contour and its bounding rectangle to the list
    
totalBars = len(bar_contours)  # Total number of bar contours

bar_magnitudes = []

for contour, (x, y, w, h) in bar_contours:
    mask = np.zeros_like(img_thresh)  # Create a mask for the current contour
    cv2.drawContours(mask, [contour], -1, 255, -1)  # Draw the contour on the mask
    
    mean_val = cv2.mean(gray, mask)[0]  # Calculate the mean value of the grayscale image within the contour
    bar_magnitudes.append(mean_val)  # Add the mean value to the list of bar magnitudes
    
activeBars = 1  # Initialize the count of active bars
closeness_to_first = 20  # Threshold for determining if a bar is active
rolling_average = bar_magnitudes[0]  # Initialize the rolling average with the first bar magnitude

# Determine the number of active bars
for i in range(1, len(bar_magnitudes)):
    if abs(bar_magnitudes[i] - rolling_average) < closeness_to_first:  # Check if the current bar is close to the rolling average
        rolling_average = (rolling_average + bar_magnitudes[i]) / 2  # Update the rolling average
        activeBars += 1  # Increment the count of active bars

# Print the number of active bars and total bars
print(f"{activeBars}/{totalBars}")