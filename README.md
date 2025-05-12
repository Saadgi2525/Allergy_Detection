## 🏷️ Allergy Label Scanner (Flask App)

This project is a web-based tool to help users detect allergens in product labels using OCR (Optical Character Recognition) and a personalized allergy list. Users upload an image of a product's ingredients, and the app scans the text for potential allergens based on the user's stored preferences.

---

## 🔧 Features

- 🖼️ Upload product label images.
- 📄 Extract text using Tesseract OCR.
- 🧠 Detect known allergens from user-specific allergy lists.
- 💾 Store and update user allergies using MySQL.
- 📊 Results displayed in a simple and intuitive web interface.

---

## 📁 Project Structure

├── templates/
│ ├── upload.html # Image upload form
│ └── result.html # Display OCR + allergen match
├── app.py #Main Code
├── check_allergens.py # Allergen detection logic
├── requirements.txt # Python dependencies
└── tesseract.py #Individual imaage_to_text converter

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Saadgi2525/Allergy_Detection.git
cd Allergy_Detection

### 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set up MySQL database
CREATE TABLE users_allergies (
    user_name VARCHAR(255) PRIMARY KEY,
    allergies TEXT
);

### 🧪 Usage (Local)
python app.py


# NOTE:: This project can also use OCRSpace API for Image to Text Conversion. Check the OCRSpace.py 
# to understand the right usage and then uncomment the code in app.py to implement using this API.
# Do not forget to create your own API before opting this method. 

