import numpy as np
import traceback
from PIL import Image
import pytesseract
import cv2
import os


def get_type_structure(format_file, user_id):
    try:
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        image=cv2.imread(f'{user_id}.{format_file}')
        gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filename=f"{user_id}.{format_file}".format(os.getpid())
        cv2.imwrite(filename, gray)
        text=pytesseract.image_to_string(Image.open(filename),  lang='rus')
        #os.remove(filename)
        if ('фактура' or 'налог') in text.lower():
            return 'Счёт-фактуры'
        elif 'фактура' not in text.lower() and ('счет' or 'счёт' or 'отчет') in text.lower():
            return 'Счёт'
        else:
            return 'Документ не распознан. Ошибка'
    except Exception:
        print(traceback.format_exc())
