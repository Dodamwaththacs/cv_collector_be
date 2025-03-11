import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from app.database import get_users_not_replied, set_replied
import pytz



def send_email(user):

    try:
        set_replied(user.id)
    except Exception as e:
        print(f"Error setting replied for user {user.id}: {e}")
        return

    sender_email = "teamnova.uom@gmail.com"
    sender_password = "nhcc edhh xpck zdbe"

    subject = "Your CV Status"
    body = "Your CV is under review. We will contact you if there is any possibility of a match."


    # Gmail SMTP Server
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    # Create email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = user.email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)  # Login
        server.sendmail(sender_email, user.email, msg.as_string())  # Send email
        server.quit()  # Close connection
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")


def get_users_to_send_message():
    # Get the current UTC time
    now_utc = datetime.utcnow()

    # Query users who have not replied
    users = get_users_not_replied()

    users_to_notify = []

    for user in users:
        try:
            # Convert user's timestamp to their timezone
            user_tz = pytz.timezone(user.timezone)
            user_time = user.timestamp.replace(tzinfo=pytz.utc).astimezone(user_tz)

            # Define the convenient time window (e.g., 9 AM - 6 PM user local time)
            convenient_start = user_tz.localize(datetime(user_time.year, user_time.month, user_time.day, 9, 0, 0))
            convenient_end = user_tz.localize(datetime(user_time.year, user_time.month, user_time.day, 18, 0, 0))

            # Check if at least one day has passed
            if now_utc - user.timestamp >= timedelta(days=1):
                # Check if current local time is within the convenient window
                now_user_time = datetime.now(user_tz)
                if convenient_start.time() <= now_user_time.time() <= convenient_end.time():
                    users_to_notify.append(user)

        except Exception as e:
            print(f"Error processing user {user.id}: {e}")

    for user in users_to_notify:
        send_email(user)

    return users_to_notify