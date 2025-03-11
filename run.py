from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.email_service import get_users_to_send_message
app = create_app()

def scheduled_task():
    with app.app_context():
        get_users_to_send_message()
        print("Scheduled task")

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_task, trigger="interval", seconds=30)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

