import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email):

    sender_email = "teamnova.uom@gmail.com"
    sender_password = "nhcc edhh xpck zdbe"

    subject = "Test Email from Python"
    body = "Hello, this is a test email sent using Python and Gmail SMTP."


    # Gmail SMTP Server
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    # Create email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)  # Login
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send email
        server.quit()  # Close connection
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")