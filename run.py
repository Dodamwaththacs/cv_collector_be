from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = create_app()

def scheduled_task():
    print(f"Scheduled task executed at {datetime.now()}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_task, trigger="interval", seconds=30)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)  # Keep debug=True for local testing