import pytesseract
from PIL import Image

img = Image.open("your_image_path")  # Test with a known image
text = pytesseract.image_to_string(img)
print(text)