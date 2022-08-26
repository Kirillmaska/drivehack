import numpy as np
import traceback
from PIL import Image
import pytesseract
import cv2
import os


def rotate_image(image, angle):
    (height, width) = image.shape[:2]
    (cX, cY) = (width / 2, height / 2)
    matrix = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(matrix[0, 0])
    sin = np.abs(matrix[0, 1])
    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))
    matrix[0, 2] += (new_width / 2) - cX
    matrix[1, 2] += (new_height / 2) - cY
    return cv2.warpAffine(image, matrix, (new_width, new_height))


def get_type_structure(format_file, user_id):
    try:
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        image=cv2.imread(f'{user_id}.{format_file}')
        gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        """        x, y, w, h=0, 0, image.shape[1], image.shape[0]

        top_half=((x, y), (x + w, y + h / 2))
        bottom_half=((x, y + h / 2), (x + w, y + h))

        top_x1, top_y1=top_half[0]
        top_x2, top_y2=top_half[1]
        bottom_x1, bottom_y1=bottom_half[0]
        bottom_x2, bottom_y2=bottom_half[1]
        blurred=cv2.GaussianBlur(gray, (3, 3), 0)
        thresh=cv2.threshold(blurred, 110, 255, cv2.THRESH_BINARY_INV)[1]
        top_image=thresh[top_y1:top_y2, top_x1:top_x2]
        bottom_image=thresh[bottom_y1:bottom_y2, bottom_x1:bottom_x2]

        top_pixels=cv2.countNonZero(top_image)
        bottom_pixels=cv2.countNonZero(bottom_image)
        if top_pixels > bottom_pixels:
            gray=rotate_image(gray, 180)
        """
        filename=f"{user_id}.{format_file}".format(os.getpid())
        cv2.imwrite(filename, gray)
        text=pytesseract.image_to_string(Image.open(filename),  lang='rus')
        os.remove(filename)
        if ('фактура' or 'налог') in text.lower():
            return 'Счёт-фактуры'
        elif 'фактура' not in text.lower() and ('счет' or 'счёт' or 'отчет') in text.lower():
            return 'Счёт'
        else:
            return 'Документ не распознан. Ошибка'
    except Exception:
        print(traceback.format_exc())
