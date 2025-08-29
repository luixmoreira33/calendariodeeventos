"""
Django management command to test profession integration.

Usage:
    python manage.py test_profession_integration
"""

from django.core.management.base import BaseCommand
from setup.models import Profession
from calendarrequest.models import UserRequest
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Test profession integration across the application'

    def handle(self, *args, **options):
        self.stdout.write("🧪 TESTING PROFESSION INTEGRATION")
        self.stdout.write("="*50)
        
        # Test 1: Check if professions exist
        profession_count = Profession.objects.filter(is_active=True).count()
        self.stdout.write(f"✅ Active professions in database: {profession_count}")
        
        if profession_count == 0:
            self.stdout.write(
                self.style.WARNING("⚠️  No active professions found. Run 'python manage.py load_professions' first.")
            )
            return
        
        # Test 2: Show some profession examples
        sample_professions = Profession.objects.filter(is_active=True)[:5]
        self.stdout.write("\n📋 Sample professions:")
        for prof in sample_professions:
            self.stdout.write(f"  - {prof.name}")
        
        # Test 3: Check UserRequest with profession
        user_requests_count = UserRequest.objects.count()
        user_requests_with_profession = UserRequest.objects.exclude(profession__isnull=True).count()
        
        self.stdout.write(f"\n📊 UserRequest statistics:")
        self.stdout.write(f"  - Total user requests: {user_requests_count}")
        self.stdout.write(f"  - With profession: {user_requests_with_profession}")
        self.stdout.write(f"  - Without profession: {user_requests_count - user_requests_with_profession}")
        
        # Test 4: Check CustomUser with profession
        custom_users_count = CustomUser.objects.count()
        users_with_profession = CustomUser.objects.exclude(profession__isnull=True).count()
        
        self.stdout.write(f"\n👥 CustomUser statistics:")
        self.stdout.write(f"  - Total users: {custom_users_count}")
        self.stdout.write(f"  - With profession: {users_with_profession}")
        self.stdout.write(f"  - Without profession: {custom_users_count - users_with_profession}")
        
        # Test 5: Check form integration
        try:
            from calendarrequest.forms import UserRequestForm
            form = UserRequestForm()
            profession_field = form.fields.get('profession')
            
            if profession_field:
                profession_choices_count = profession_field.queryset.count()
                self.stdout.write(f"\n📝 Form integration:")
                self.stdout.write(f"  - Profession choices available: {profession_choices_count}")
                self.stdout.write(f"  - Empty label: '{profession_field.empty_label}'")
            else:
                self.stdout.write(
                    self.style.ERROR("\n❌ Profession field not found in UserRequestForm")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"\n❌ Error testing form integration: {str(e)}")
            )
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS("🎉 Profession integration test completed!")
        )
