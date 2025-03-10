from flask import Blueprint, request, jsonify
import tempfile
import os
from app.services.goolesheet_service import store_data
from app.services.pdf_service import extract_cv_data
from app.models import User
from app.database import db

cv_bp = Blueprint('cv_bp', __name__)

@cv_bp.route('/parse_cv', methods=['POST'])
def parse_cv_endpoint():

    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400

    pdf_file = request.files['pdf']
    name = request.form.get('name')
    email = request.form.get('email')

    print(name)
    print(email)

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

        cv_data = extract_cv_data(temp_pdf_path)

        # cv_data = "CV Data"
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


@cv_bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully',
                    'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}})