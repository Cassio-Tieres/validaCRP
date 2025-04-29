from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = Image.open('img/crp04_frente.jpg')

print(pytesseract.image_to_string(img, lang='por'))