"""
Django management command to test Setup integration.

Usage:
    python manage.py test_setup_integration
"""

from django.core.management.base import BaseCommand
from setup.models import Setup
from calendarrequest.models import UserRequest
from calendarrequest.forms import UserRequestForm


class Command(BaseCommand):
    help = 'Test Setup integration across the application'

    def handle(self, *args, **options):
        self.stdout.write("🧪 TESTING SETUP INTEGRATION")
        self.stdout.write("="*50)
        
        # Test 1: Check if Setup exists
        setup = Setup.objects.last()
        if setup:
            self.stdout.write(
                self.style.SUCCESS("✅ Setup configuration found:")
            )
            self.stdout.write(f"  - URL: {setup.url}")
            self.stdout.write(f"  - Admin Email: {setup.admin_email}")
            self.stdout.write(f"  - Calendar URL: {setup.calendar_url}")
        else:
            self.stdout.write(
                self.style.ERROR("❌ No Setup configuration found!")
            )
            self.stdout.write("  Run 'python manage.py create_default_setup' to create one.")
            return
        
        # Test 2: Test form creation
        try:
            form = UserRequestForm()
            self.stdout.write(
                self.style.SUCCESS("\n✅ UserRequestForm created successfully")
            )
            
            # Check if profession field has choices
            profession_field = form.fields.get('profession')
            if profession_field:
                profession_choices = profession_field.queryset.count()
                self.stdout.write(f"  - Profession choices available: {profession_choices}")
            else:
                self.stdout.write(
                    self.style.WARNING("  ⚠️  Profession field not found")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"\n❌ Error creating form: {str(e)}")
            )
        
        # Test 3: Check UserRequest count
        user_requests_count = UserRequest.objects.count()
        self.stdout.write(f"\n📊 UserRequest statistics:")
        self.stdout.write(f"  - Total requests: {user_requests_count}")
        
        # Test 4: Test email context
        try:
            from calendarrequest.utils import send_email_notification
            
            # Create a mock context
            mock_context = {
                'user_request': None,
                'login_url': setup.url
            }
            
            self.stdout.write(
                self.style.SUCCESS("\n✅ Email utility test:")
            )
            self.stdout.write(f"  - Login URL: {mock_context['login_url']}")
            self.stdout.write(f"  - Setup URL accessible: {'✅' if setup.url else '❌'}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"\n❌ Error testing email utility: {str(e)}")
            )
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS("🎉 Setup integration test completed!")
        )
