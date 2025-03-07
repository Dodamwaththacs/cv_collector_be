from flask import Blueprint, request, jsonify
import tempfile
import os
from app.services.pdf_service import extract_cv_data
from app.services.storage_service import upload_file_to_s3
from app.services.email_service import send_email
from app.services.goolesheet_service import store_data

cv_bp = Blueprint('cv_bp', __name__)

@cv_bp.route('/parse_cv', methods=['POST'])
def parse_cv_endpoint():
    """API endpoint to parse CV from PDF."""
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400

    pdf_file = request.files['pdf']

    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            pdf_file.save(temp_pdf.name)
            temp_pdf_path = temp_pdf.name

        # Generate a unique S3 key
        s3_key = f"uploads/{os.path.basename(temp_pdf_path)}"
        # s3_url = upload_file_to_s3(temp_pdf_path, s3_key)
        s3_url = "https://s3.amazonaws.com/your-bucket-name/uploads/your-file-name.pdf"

        # cv_data = extract_cv_data(temp_pdf_path)

        cv_data = "CV Data"
        # send_email("chamikasandun3131@gmail.com")
        store_data()

        # Clean up the temporary file
        os.unlink(temp_pdf_path)

        if cv_data:
            return jsonify({'cv_data': cv_data, 's3_url': s3_url})
        else:
            return jsonify({'error': 'Failed to parse CV'}), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500