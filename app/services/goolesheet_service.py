import gspread
import json
import uuid
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from JSON key file (replace 'your-key.json' with the actual path)
SERVICE_ACCOUNT_FILE = "service.json"

# Define the scope for Google Sheets API
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
client = gspread.authorize(credentials)

# Open the Google Sheet (replace with your actual Google Sheet name)
SPREADSHEET_NAME = "test"
spreadsheet = client.open(SPREADSHEET_NAME)

# Function to store applicant data
def store_applicant(cv_data, pdf_url):
    try:
        # Get or create the main sheet for applicants
        try:
            sheet = spreadsheet.worksheet("Applicants")
        except gspread.exceptions.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="Applicants", rows="1000", cols="10")
            sheet.append_row(["Applicant ID", "Name", "Email", "Phone", "Address", "Education", "Projects", "Skills", "Certifications", "CV URL"])

        # Generate a unique ID for the applicant
        applicant_id = str(uuid.uuid4())

        # Extract applicant data
        personal_info = cv_data["personal_information"]
        education = cv_data["education"]
        projects = cv_data["projects"]
        qualifications = cv_data["qualifications"]

        # Convert lists to JSON strings or comma-separated values
        education_str = json.dumps(education)  # Store as JSON
        projects_str = json.dumps(projects)  # Store as JSON
        skills_str = ", ".join(qualifications["skills"])  # Store as CSV
        certifications_str = ", ".join(qualifications["certifications"]) if qualifications["certifications"] else "None"

        # Append data to Google Sheet
        sheet.append_row([
            applicant_id,
            personal_info["name"],
            personal_info["email"],
            personal_info["phone"],
            personal_info["address"],
            education_str,
            projects_str,
            skills_str,
            certifications_str,
            pdf_url
        ])

        print(f"Applicant {personal_info['name']} stored successfully with ID: {applicant_id}")

    except Exception as e:
        print(f"Error storing applicant data: {e}")

