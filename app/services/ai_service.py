import google.generativeai as genai
import json
import re
from flask import current_app
from app.config import Config

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

def parse_cv(cv_text):

    print("inside parse_cv")
    """Parses CV using Gemini AI model."""
    if not cv_text:
        return None

    # Updated way to create a model instance
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use the correct model name

    prompt = f"""
    Extract the following information from the CV text and return it in **valid JSON format**:

    - **Personal Information**: name, email, phone number, address  
    - **Education**: degrees, institutions, dates  
    - **Qualifications**: skills, certifications  
    - **Projects**: project names, descriptions  

    **CV Text:**  
    {cv_text}  

    The output **must strictly follow** this JSON structure:  
    ```json
    {{
      "personal_information": {{
        "name": "",
        "email": "",
        "phone": "",
        "address": ""
      }},
      "education": [
        {{
          "degree": "",
          "institution": "",
          "date": ""
        }}
      ],
      "qualifications": {{
        "skills": [],
        "certifications": []
      }},
      "projects": [
        {{
          "name": "",
          "description": ""
        }}
      ]
    }}
    """


    try:
        response = model.generate_content(prompt)

        print("gemini responce",response)

        if hasattr(response, 'text'):
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error with AI parsing: {e}")
        return None

def parse_json(json_response):
    """Parses JSON response safely."""
    try:
        if not isinstance(json_response, str):
            return None

        # Extract JSON using regex (if wrapped in triple backticks)
        match = re.search(r'```json\n(.*?)\n```', json_response, re.DOTALL)
        if match:
            json_response = match.group(1)  # Extract only the JSON content

        return json.loads(json_response)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None