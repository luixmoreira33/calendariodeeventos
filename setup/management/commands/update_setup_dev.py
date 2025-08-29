"""
Django management command to update Setup with development values.

Usage:
    python manage.py update_setup_dev
"""

from django.core.management.base import BaseCommand
from setup.models import Setup


class Command(BaseCommand):
    help = 'Update Setup with development values'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default='http://localhost:8000',
            help='System URL for development'
        )
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@localhost.com',
            help='Admin email for development'
        )
        parser.add_argument(
            '--calendar-url',
            type=str,
            default='https://calendar.google.com/calendar',
            help='Google Calendar URL'
        )

    def handle(self, *args, **options):
        self.stdout.write("🔧 UPDATING SETUP FOR DEVELOPMENT")
        self.stdout.write("="*50)
        
        setup = Setup.objects.last()
        if not setup:
            self.stdout.write(
                self.style.ERROR("❌ No Setup configuration found!")
            )
            self.stdout.write("  Run 'python manage.py create_default_setup' first.")
            return
        
        # Update values
        old_url = setup.url
        old_admin_email = setup.admin_email
        old_calendar_url = setup.calendar_url
        
        setup.url = options['url']
        setup.admin_email = options['admin_email']
        setup.calendar_url = options['calendar_url']
        setup.save()
        
        self.stdout.write(
            self.style.SUCCESS("✅ Setup updated successfully!")
        )
        self.stdout.write(f"\n📝 Changes made:")
        self.stdout.write(f"  - URL: {old_url} → {setup.url}")
        self.stdout.write(f"  - Admin Email: {old_admin_email} → {setup.admin_email}")
        self.stdout.write(f"  - Calendar URL: {old_calendar_url} → {setup.calendar_url}")
        
        self.stdout.write(f"\n🔗 Current configuration:")
        self.stdout.write(f"  - System URL: {setup.url}")
        self.stdout.write(f"  - Admin Email: {setup.admin_email}")
        self.stdout.write(f"  - Calendar URL: {setup.calendar_url}")
        
        self.stdout.write(
            self.style.WARNING("\n⚠️  Remember to update these values for production!")
        )
