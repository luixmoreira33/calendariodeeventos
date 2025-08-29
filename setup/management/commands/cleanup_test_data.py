"""
Django management command to cleanup test data.

Usage:
    python manage.py cleanup_test_data [--force]
"""

from django.core.management.base import BaseCommand
from calendarrequest.models import UserRequest
from accounts.models import CustomUser, UserLodge
from setup.models import Setup


class Command(BaseCommand):
    help = 'Cleanup test data from the system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force cleanup without confirmation'
        )

    def handle(self, *args, **options):
        self.stdout.write("🧹 CLEANING UP TEST DATA")
        self.stdout.write("="*50)
        
        # Check if this is a production environment
        setup = Setup.objects.last()
        if setup and 'localhost' not in setup.url and 'test' not in setup.url.lower():
            self.stdout.write(
                self.style.ERROR("❌ This appears to be a production environment!")
            )
            self.stdout.write("   Aborting cleanup for safety.")
            return
        
        # Count items to be cleaned
        test_user_requests = UserRequest.objects.filter(
            email__in=['fulano@silva.com', 'fernandovalentedev@gmail.com']
        )
        test_users = CustomUser.objects.filter(
            email__in=['fulano@silva.com', 'fernandovalentedev@gmail.com']
        )
        
        if not test_user_requests.exists() and not test_users.exists():
            self.stdout.write("✅ No test data found to clean up.")
            return
        
        self.stdout.write(f"📋 Items to be cleaned:")
        self.stdout.write(f"  - Test UserRequests: {test_user_requests.count()}")
        self.stdout.write(f"  - Test Users: {test_users.count()}")
        
        if not options['force']:
            confirm = input("\n❓ Are you sure you want to proceed? (yes/no): ")
            if confirm.lower() not in ['yes', 'y']:
                self.stdout.write("❌ Cleanup cancelled.")
                return
        
        # Cleanup test data
        try:
            # Delete test users (this will cascade to UserLodge)
            deleted_users = test_users.count()
            test_users.delete()
            self.stdout.write(f"✅ Deleted {deleted_users} test users")
            
            # Delete test user requests
            deleted_requests = test_user_requests.count()
            test_user_requests.delete()
            self.stdout.write(f"✅ Deleted {deleted_requests} test user requests")
            
            self.stdout.write(
                self.style.SUCCESS(f"\n🎉 Cleanup completed successfully!")
            )
            self.stdout.write(f"   - Users deleted: {deleted_users}")
            self.stdout.write(f"   - Requests deleted: {deleted_requests}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error during cleanup: {e}")
            )
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS("🎉 Test data cleanup completed!")
        )
