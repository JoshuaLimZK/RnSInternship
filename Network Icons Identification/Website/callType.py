import cv2
import pytesseract

def identify_call_service(image_dir, coordinates):
    img = cv2.imread(image_dir)[coordinates[0]:coordinates[1], coordinates[2]:coordinates[3]]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thres,thres_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    # save thres_img
    cv2.imwrite('static/thres_img_call.png', thres_img)
    text = pytesseract.image_to_string(thres_img, config='--user-words words.txt --psm 11 network-icon').replace(' ', '')
    print(f"Call Service Type: {text}")
    if 'LTE' in text:
        return 'VoLTE'
    elif 'NR' in text:
        return 'VoNR'
    else:
        return 'Call Service Unknown'