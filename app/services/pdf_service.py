import PyPDF2
from app.services.ai_service import parse_cv, parse_json

def pdf_to_text(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip() if text else None
    except (FileNotFoundError, PyPDF2.PdfReadError) as e:
        print(f"Error reading PDF: {e}")
        return None

def extract_cv_data(pdf_path):
    """Extracts CV data from a PDF file."""
    cv_text = pdf_to_text(pdf_path)
    if not cv_text:
        return None

    json_response = parse_cv(cv_text)
    if not json_response:
        return None

    return parse_json(json_response)