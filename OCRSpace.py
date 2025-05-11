import requests

# Replace with your OCR.space API key
api_key = 'your_api_key'

# Path to your image file
image_path = 'your_image_path'

# Read and send the image
with open(image_path, 'rb') as image_file:
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={'filename': image_file},
        data={'apikey': api_key}
    )

# Parse the response
result = response.json()
text = result.get('ParsedResults', [{}])[0].get('ParsedText', 'No text found')
print("Extracted Text:")
print(text)
