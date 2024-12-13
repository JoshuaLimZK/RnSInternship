import cv2
import pytesseract

def identify_network_type(image_dir, coordinates):
    img = cv2.imread(image_dir)[coordinates[0]:coordinates[1], coordinates[2]:coordinates[3]]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # upscale the image
    scale_factor = 1
    scaled = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    
    # threshold the image using OTSU into a binary image
    thres,thres_img = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    
    # save thres_img
    cv2.imwrite('static/thres_img_network.png', thres_img)
    text = pytesseract.image_to_string(thres_img, config='--user-words words.txt --psm 7 network-icon').replace(' ', '')
    print(f"Network Type: {text}")
    if any(s in text for s in ['4G', 'AG', '46', 'A6', 'LTE']):
        return '4G'
    elif '5G' in text or '56' in text:
        return '5G'
    else:
        return 'Network Unknown'