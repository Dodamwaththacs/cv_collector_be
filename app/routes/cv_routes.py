from datetime import timezone
from flask import Blueprint, request, jsonify
import tempfile
import os
from app.services.storage_service import upload_file_to_s3
from app.services.webhook_service import send_cv_webhook
from app.services.goolesheet_service import store_applicant
from app.services.pdf_service import extract_cv_data
from app.database import get_user_by_email_or_mobile, add_user

cv_bp = Blueprint('cv_bp', __name__)

@cv_bp.route('/parse_cv', methods=['POST'])
def parse_cv_endpoint():

    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400

    pdf_file = request.files['pdf']
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    timezone = request.form.get('timezone')

    required_fields = {'name': name, 'email': email, 'phone': phone, 'timezone': timezone}
    missing_fields = [field for field, value in required_fields.items() if not value]

    if not pdf_file:
        return jsonify({'error': 'No PDF file provided'}), 400

    if pdf_file.filename == '':
        return jsonify({'error': 'Empty PDF file provided'}), 400

    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    if get_user_by_email_or_mobile (email, phone):
        return jsonify({'error': 'User already exists'}), 400


    try:
        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            pdf_file.save(temp_pdf.name)
            temp_pdf_path = temp_pdf.name

        # Generate a unique S3 key
        s3_key = f"uploads/{os.path.basename(temp_pdf_path)}"
        s3_url = upload_file_to_s3(temp_pdf_path, s3_key)
        # s3_url = "https://s3.amazonaws.com/your-bucket-name/uploads/your-file-name.pdf"

        cv_data = extract_cv_data(temp_pdf_path)

        # cv_data = "CV Data"
        store_applicant(cv_data, s3_url)


        add_user (name, email, phone, timezone)
        # send_cv_webhook (cv_data, name, email)
        # Clean up the temporary file
        os.unlink(temp_pdf_path)


        if cv_data:
            return jsonify({'cv_data': cv_data, 's3_url': s3_url})
        else:
            return jsonify({'error': 'Failed to parse CV'}), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


# @cv_bp.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.json
#     if not data or 'name' not in data or 'email' not in data:
#         return jsonify({'error': 'Invalid input'}), 400
#
#     new_user = User(name=data['name'], email=data['email'])
#     db.session.add(new_user)
#     db.session.commit()
#
#     return jsonify({'message': 'User added successfully',
#                     'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}})
#
# @cv_bp.route('/get_users', methods=['GET'])
# def get_users():
#     users = get_all_users()
#     return jsonify({'users': [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]})