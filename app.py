from flask import Flask, request, render_template
import cv2
import pytesseract
import numpy as np
import mysql.connector
from check_allergens import check_allergens
from PIL import Image

app = Flask(__name__)

# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        user='root',
        host='localhost',
        password='Saadgi@251103',
        database='allergens'
    )

def insert_allergen(user_name, allergies):
    """Insert or update user allergies in the MySQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT allergies FROM users_allergies WHERE user_name = %s", (user_name,))
    result = cursor.fetchone()
    
    if result:
        # Merge new allergens with existing ones
        existing_allergens = set(result[0].split(', '))
        new_allergens = set(allergies.split(', '))
        updated_allergens = ', '.join(existing_allergens | new_allergens)  # Union set
        
        # Update database
        cursor.execute("UPDATE users_allergies SET allergies = %s WHERE user_name = %s", (updated_allergens, user_name))
    else:
        # Insert new record
        cursor.execute("INSERT INTO users_allergies (user_name, allergies) VALUES (%s, %s)", (user_name, allergies))
    
    conn.commit()
    conn.close()

def get_allergens(user_name):
    """Fetch allergens from the database specific to the given user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch allergens only for the specified user
    cursor.execute("SELECT allergies FROM users_allergies WHERE user_name = %s", (user_name,))
    result = cursor.fetchall()
    
    conn.close()

    # Convert results into a list of allergens
    allergens = []
    for row in result:
        allergens.extend(row[0].lower().split(', '))  # Split stored allergens
    
    return allergens

    # Convert results into a list of allergens
    allergens = []
    for row in result:
        allergens.extend(row[0].lower().split(', '))  # Split stored allergens
    
    return allergens


import requests
#*******************Image to Text using OCR.space******************#
# @app.route('/', methods=['GET', 'POST'])
# def upload_image():
#     if request.method == 'POST':
#         user_name = request.form.get('user_name', 'Unknown User')
#         user_allergies = request.form.get('allergies', '').split(',')
#         user_allergies = ', '.join([allergy.strip().lower() for allergy in user_allergies])

#         # Insert user allergies into MySQL
#         insert_allergen(user_name, user_allergies)

#         # Get the image from the form
#         image = request.files['file']
#         api_key = 'your_api_key'  # Replace with your actual API key
        
#         # Send image to OCR.space
#         response = requests.post(
#             'https://api.ocr.space/parse/image',
#             files={'filename': image},
#             data={'apikey': api_key,
#             'filetype': 'JPG','PNG','JPEG'}
#         )
        
#         # Extract text
#         result = response.json()
#         print("Response:", result)
#         text = result.get('ParsedResults', [{}])[0].get('ParsedText', 'No text found')

#         stored_allergens = get_allergens()

#         # Check for allergens
#         found_allergens = check_allergens(text, stored_allergens)

#         # Debugging output
#         print("Extracted Text:", text)
#         print("Allergens Found:", found_allergens)

#         return render_template('result.html', user_name=user_name, text=text, allergens=found_allergens)

#     return render_template('upload.html')

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Unknown User')
        user_allergies = request.form.get('allergies', '').split(',')
        user_allergies = ', '.join([allergy.strip().lower() for allergy in user_allergies])

        # Insert user allergies into MySQL
        insert_allergen(user_name, user_allergies)

        # Get the image from the form
        image = request.files['file']

        # Extract text using Tesseract
        img = Image.open(image)
        text = pytesseract.image_to_string(img)


        # Check if text is readable
        if text.strip() == "":
            print("Tesseract could not extract readable text. Please upload a clearer image.", "warning")
            return render_template('upload.html')

        stored_allergens = get_allergens(user_name)
        found_allergens = check_allergens(text, stored_allergens)

        print("Extracted Text:", text)
        print("Allergens Found:", found_allergens)

        return render_template('result.html', user_name=user_name, text=text, allergens=found_allergens)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)