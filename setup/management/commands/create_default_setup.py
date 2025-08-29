"""
Django management command to create default Setup configuration.

Usage:
    python manage.py create_default_setup
"""

from django.core.management.base import BaseCommand
from setup.models import Setup


class Command(BaseCommand):
    help = 'Create default Setup configuration if none exists'

    def handle(self, *args, **options):
        self.stdout.write("🔧 CREATING DEFAULT SETUP")
        self.stdout.write("="*50)
        
        # Check if Setup already exists
        if Setup.objects.exists():
            setup = Setup.objects.last()
            self.stdout.write(
                self.style.WARNING(f"⚠️  Setup already exists:")
            )
            self.stdout.write(f"  - URL: {setup.url}")
            self.stdout.write(f"  - Admin Email: {setup.admin_email}")
            self.stdout.write(f"  - Calendar URL: {setup.calendar_url}")
            return
        
        # Create default Setup
        try:
            setup = Setup.objects.create(
                url='http://localhost:8000',
                calendar_url='https://calendar.google.com/calendar',
                admin_email='admin@example.com'
            )
            
            self.stdout.write(
                self.style.SUCCESS("✅ Default Setup created successfully!")
            )
            self.stdout.write(f"  - URL: {setup.url}")
            self.stdout.write(f"  - Admin Email: {setup.admin_email}")
            self.stdout.write(f"  - Calendar URL: {setup.calendar_url}")
            
            self.stdout.write(
                self.style.WARNING("\n⚠️  IMPORTANT: Please update these values in the admin panel!")
            )
            self.stdout.write("   Go to /admin/setup/setup/ and update with your actual values.")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating Setup: {str(e)}")
            )
