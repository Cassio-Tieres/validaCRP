from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_image(image_path):
    imagem = Image.open(image_path)
    texto = pytesseract.image_to_string(imagem, lang='por')
    return texto.strip()