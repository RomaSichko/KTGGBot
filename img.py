import cv2
import pytesseract
import json
import codecs
import shtrih_kod

def get_username(img_name):
    # Путь для подключения tesseract
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\admin\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

    # Подключение фото
    img = cv2.imread(img_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Будет выведен весь текст с картинки
    config = r'--oem 3 --psm 6'
    text = str(pytesseract.image_to_string(img, config=config, lang='ukr'))
    # print(text)
    # json
    text_json = json.load(codecs.open("students.json", 'r', 'utf-8-sig'))

    list_items = []

    user_name = ""
    try:
        check_barcode = int(shtrih_kod.BarcodeReader(img_name))
    except ValueError:
        check_barcode = 0
    # check_barcode = int(shtrih_kod.BarcodeReader(img_name))

    # check json
    if check_barcode:
        for i in text_json:
            name = i["Здобувач"].split()
            
            name[0], name[1] = name[1], name[0]
            stud_ticket = i["Студентський (учнівський) квиток"].split()[1]
            # print(name, stud_ticket)
            if stud_ticket == str(check_barcode) or (name[0] in text and name[1] in text and stud_ticket in text):
                user_name = " ".join(name[:2])

    if user_name == "":
        return "error"
    else:
        return user_name

# print(get_username("image2.jpg"))
