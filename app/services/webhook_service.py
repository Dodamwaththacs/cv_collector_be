import requests
import json
from datetime import datetime
from flask import current_app
import logging


def send_cv_webhook(cv_data, name, email):
    try:
        webhook_url = "https://rnd-assignment.automations-3d6.workers.dev/"

        payload = {
            "cv_data": {
                "personal_info": cv_data["personal_information"],
                "education": cv_data["education"],
                "qualifications": cv_data["qualifications"],
                "projects": cv_data["projects"],
                "cv_public_link": "https://s3.amazonaws.com/bucket-name/uploads/file-name.pdf"
            },

            "metadata": {
                "applicant_name": name,
                "email": email,
                "status": "prod",
                "cv_processed": True,
                "processed_timestamp": "2025-02-28T12:00:00Z"
            }
        }

        # Set headers for the request
        headers = {
            'Content-Type': 'application/json',
            'X-Candidate-Email': "chamikasandun3131@gmail.com"
        }

        print("Sending payload:")
        print(json.dumps(payload, indent=2))

        # Send the request
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10  # 10 seconds timeout
        )



        # Check if the request was successful
        print(response.status_code)

        # Log success
        logging.info(f"Webhook successfully sent for {email}")
        print("Webhook successfully sent for")

        return True, response.json()

    except requests.exceptions.RequestException as e:
        # Log the error
        logging.error(f"Webhook request failed: {str(e)}")
        return False, str(e)

    except Exception as e:
        # Log unexpected errors
        logging.error(f"Unexpected error in webhook: {str(e)}")
        return False, str(e)