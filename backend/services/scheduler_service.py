from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from ..models import db, User, CompletedWork
from ..utils.email_service import send_reminder_email
from datetime import datetime, timedelta
import logging
import traceback

logger = logging.getLogger(__name__)

def check_and_send_reminders(app, mail):
    with app.app_context():
        try:
            completed_work = CompletedWork.query.first()
            
            if completed_work and completed_work.count > 0:
                # For every completed work, send a reminder to the token (work_number + 2)
                # When work #1 is completed, send reminder to token #3
                # When work #2 is completed, send reminder to token #4
                # When work #3 is completed, send reminder to token #5
                # etc.
                target_token_number = completed_work.count + 2
                
                # Check if reminder has already been sent for this token
                target_user = User.query.filter_by(token_number=target_token_number, reminder_sent=False).first()
                
                if target_user:
                    user_data = {
                        'token_number': target_user.token_number,
                        'name': target_user.name,
                        'email': target_user.email,
                        'work_description': target_user.work_description
                    }
                    
                    if send_reminder_email(mail, user_data):
                        target_user.reminder_sent = True
                        db.session.commit()
                        logger.info(f"Reminder sent to Token #{target_user.token_number} for completed work #{completed_work.count}")
                    else:
                        logger.error(f"Failed to send reminder to Token #{target_user.token_number}")
                        
        except Exception as e:
            error_msg = f"Error in scheduler task: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Traceback: {traceback.format_exc()}")

def start_scheduler(app, mail):
    try:
        # Use ThreadPoolExecutor which is compatible with Windows
        executors = {
            'default': ThreadPoolExecutor(20),
        }
        
        scheduler = BackgroundScheduler(executors=executors)
        
        scheduler.add_job(
            func=lambda: check_and_send_reminders(app, mail),
            trigger='interval',
            minutes=1,
            id='reminder_check',
            name='Check and send reminders every minute',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("Scheduler started successfully")
        
        return scheduler
    except Exception as e:
        error_msg = f"Error starting scheduler: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None