import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.conf import settings
from setup.models import Setup
from calendarrequest.utils import send_email_notification

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarService:
    def __init__(self):
        self.service = self._get_calendar_service()
        self.calendar_id = 'primary'
        self.setup = Setup.objects.last()

    def _get_calendar_service(self):
        """Initialize and return the Google Calendar service."""
        creds = None
        token_path = os.path.join(settings.BASE_DIR, 'events', 'googlecalendar', 'token.json')
        credentials_path = os.path.join(settings.BASE_DIR, 'events', 'googlecalendar', 'credentials.json')

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(google.auth.transport.requests.Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=8080, access_type='offline', prompt='consent')
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def _send_error_notification(self, event, operation, error_message):
        """Send error notification email to admin."""

        if not self.setup or not self.setup.admin_email:
            return

        context = {
            'event': event,
            'operation': operation,
            'error_message': error_message
        }

        send_email_notification(
            subject=f'Erro no Google Calendar - {operation}',
            template_name='email/google_calendar_error.html',
            context=context,
            recipient_list=[self.setup.admin_email]
        )

    def get_last_event(self):
        """
        Get the last event from Google Calendar.
        """
        events = self.service.events().list(calendarId=self.calendar_id).execute()
        if events:
            return events['items'][0]
        return None

    def create_event(self, event):
        """
        Create a new event in Google Calendar.
        
        Args:
            event: Django Event model instance
            
        Returns:
            str: Google Calendar event ID
        """

        sumary = ''
        if event.lodge:
            sumary = f'LOJA {event.lodge.name} - {event.title}'
        else:
            sumary = event.title

        event_data = {
            'summary': sumary,
            'description': event.description,
            'location': event.address,
            'start': {
                'dateTime': event.start_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': event.end_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }
        
        try:
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event_data
            ).execute()
            return created_event.get('id')
        except Exception as e:
            error_message = str(e)
            self._send_error_notification(event, 'Criação de Evento', error_message)
            raise Exception(f"Failed to create Google Calendar event: {error_message}")

    def update_event(self, event):
        """
        Update an existing event in Google Calendar.
        
        Args:
            google_event_id (str): Google Calendar event ID
            event: Django Event model instance
            
        Returns:
            dict: Updated event data
        """
        
        event_data = {
            'summary': f'Loja: {event.lodge.name} - {event.title}',
            'description': event.description,
            'location': event.address,
            'start': {
                'dateTime': event.start_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': event.end_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }
        
        try:
            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event.google_event_id,
                body=event_data
            ).execute()
            return updated_event
        except Exception as e:
            error_message = str(e)
            self._send_error_notification(event, 'Atualização de Evento', error_message)
            raise Exception(f"Failed to update Google Calendar event: {error_message}")

    def delete_event(self, event):
        """
        Delete an event from Google Calendar.
        
        Args:
            google_event_id (str): Google Calendar event ID
            
        Returns:
            bool: True if successful
        """
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event.google_event_id
            ).execute()
            return True
        except Exception as e:
            error_message = str(e)
            self._send_error_notification(event, 'Exclusão de Evento', error_message)
            raise Exception(f"Failed to delete Google Calendar event: {error_message}")


# Helper function to get a calendar service instance
def get_calendar_service():
    return GoogleCalendarService()
