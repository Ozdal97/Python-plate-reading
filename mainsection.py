import cv2
import imutils
import numpy as np
import pytesseract
import re
def main(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    img = cv2.imread(path, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (620, 480))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # griye çevir
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blurlama
    edged = cv2.Canny(gray, 30, 200)  # Köşeleri alma
    # plakaya en yakın olan köşelerin en iyisini bulur ve onu yenı ımage aline getir
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # bütün contours alır
    for c in cnts:
        #  contour hesabu
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # eğer contoursumuz 4 köşeliyse plakamızı bulduk demektir
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print
        "No contour detected"
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    # numara olmıyan yerleri maskeleme
    mask = np.zeros(gray.shape, np.uint8)
    try:
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    except:
        return None
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Kesme işlemi
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    # Keislen bölgenin okunması
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    text = text.replace('\n', '')
    regex = re.compile('[^a-zA-Z0-9]')
    text = regex.sub("", text)
    print(path + " " + text.rstrip())


    return text
    cv2.imshow('image', img)
    cv2.imshow('Cropped', Cropped)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

