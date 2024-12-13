import cv2
import pytesseract
import argparse

# Set up argument parser to recieve image path and coordinates of the crop
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-c", "--coordinates",default=[], nargs='+', type=int, help="coordinates of the crop, format: x1 y1 x2 y2")

args = vars(ap.parse_args())

# Read image path and import image
image_path = args["image"]
image = cv2.imread(image_path)

# If coordinates are passed in the arguments, crop the image
if args["coordinates"]:
    coordinates = args["coordinates"]
    image = image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Upscale image (Set to 1 for no scaling)
scale_factor = 1
scaled = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

# Apply Otsu's thresholding to convert to binary image
_, thres_img = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Use pytesseract to extract text from image
text = pytesseract.image_to_string(thres_img, config='--user-words words.txt --psm 11 network-icon').replace(' ', '')

# Check if text contains any of the following keywords
if "LTE" in text:
    print('VoLTE') 
elif "NR" in text:
    print('VoNR')
else:
    print('Call Service Unknown')