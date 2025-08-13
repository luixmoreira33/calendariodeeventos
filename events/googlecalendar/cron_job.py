import os
import django
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from events.googlecalendar.actions import get_calendar_service
from setup.models import Setup
from calendarrequest.utils import send_email_notification

logger = logging.getLogger(__name__)


def check_last_event():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info("="*50)
    logger.info(f"Starting cron job check at {current_time}")
    logger.info("="*50)
    
    try:
        calendar_service = get_calendar_service()
        last_event = calendar_service.get_last_event()
        
        if last_event:
            logger.info(f"Last event found: {last_event.get('summary')}")
            logger.info(f"Event details: Start: {last_event.get('start', {}).get('dateTime')}")
        else:
            logger.info("No events found in the calendar")
            
    except Exception as e:
        logger.error(f"Error checking last event: {str(e)}")
        setup = Setup.objects.last()
        if setup and setup.admin_email:
            try:
                send_email_notification(
                    subject='Error checking last event',
                    template_name='email/google_calendar_error.html',
                    context={
                        'error_message': str(e),
                        'operation': 'Last event check'
                    },
                    recipient_list=[setup.admin_email]
                )
            except Exception as email_error:
                logger.error(f"Error sending error notification: {str(email_error)}")
    
    logger.info("="*50)
    logger.info(f"Cron job check completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*50 + "\n")

if __name__ == '__main__':
    check_last_event()
