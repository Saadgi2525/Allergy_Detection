import re

def check_allergens(text, user_allergies):
    found_allergens = set()  # Use a set to avoid duplicates
    text = text.lower()  # Convert extracted text to lowercase
    
    for allergy in user_allergies:
        allergy = allergy.lower().strip()  # Ensure uniform matching
        
        # Use regex to match whole words
        if re.search(r'\b' + re.escape(allergy) + r'\b', text):
            found_allergens.add(allergy)
    
    return list(found_allergens)  # Convert set back to list if needed