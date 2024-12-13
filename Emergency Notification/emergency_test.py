try:
    import pytesseract
except ImportError:
    print("pytesseract is not installed, please install it using 'pip install pytesseract'")
    exit()
try:
    import cv2
except ImportError:
    print("opencv-python is not installed, please install it using 'pip install opencv-python'")
    exit()

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-w", "--words-list", required=True, help="path to words list text file")
ap.add_argument("-c", "--min-conf", type=int, default=90, help="min confidence value, default = 90")
ap.add_argument("-l", "--lang", default="eng", help="language to be used, default = eng")
ap.add_argument("-d", "--date", default="", help="Date of message in format DD/MM/YYYY, optional")

args = vars(ap.parse_args())

image_path = args["image"]

image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thres_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

language = args["lang"]

words_list = []
with open(args["words_list"], "r") as f:
    words_list = f.read().split("\n")
    
presence_list = []
    
for i in range(len(words_list)):
    words_list[i] = words_list[i].lower()
    words_list[i] = words_list[i].split(" ")
    presence_list.append([False] * len(words_list[i]))

data = pytesseract.image_to_data(thres_img, output_type=pytesseract.Output.DICT, lang=language)
filtered_data = []
for a in range(len(data["text"])):
    conf = int(data["conf"][a])
    if conf > args["min_conf"]:
        for i in range(len(words_list)):
            for j in range(len(words_list[i])):
                if words_list[i][j] in data["text"][a].lower():
                    presence_list[i][j] = True

text = pytesseract.image_to_string(thres_img, lang=language)
          
passed = False
                
for i in range(len(words_list)):
    if all(presence_list[i]):
        passed = True
        break
    
if passed:
    print("Pass")
else:
    print("Fail")
