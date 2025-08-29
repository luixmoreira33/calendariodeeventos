"""
Django management command to test user creation from UserRequest.

Usage:
    python manage.py test_user_creation
"""

from django.core.management.base import BaseCommand
from calendarrequest.models import UserRequest
from accounts.models import CustomUser, UserLodge
from lodge.models import Lodge
from setup.models import Setup


class Command(BaseCommand):
    help = 'Test user creation from UserRequest approval'

    def handle(self, *args, **options):
        self.stdout.write("🧪 TESTING USER CREATION FROM USERREQUEST")
        self.stdout.write("="*50)
        
        # Check Setup configuration
        setup = Setup.objects.last()
        if not setup:
            self.stdout.write(
                self.style.ERROR("❌ No Setup configuration found!")
            )
            return
        
        self.stdout.write(f"✅ Setup found: {setup.url}")
        
        # Check if there are any UserRequests
        user_requests = UserRequest.objects.all()
        if not user_requests.exists():
            self.stdout.write(
                self.style.WARNING("⚠️  No UserRequest found. Create one first.")
            )
            return
        
        self.stdout.write(f"📋 Found {user_requests.count()} UserRequest(s)")
        
        # Check existing users
        existing_users = CustomUser.objects.all()
        self.stdout.write(f"👥 Existing users: {existing_users.count()}")
        
        # Check existing lodges
        existing_lodges = Lodge.objects.all()
        self.stdout.write(f"🏠 Existing lodges: {existing_lodges.count()}")
        
        # Show sample UserRequest
        sample_request = user_requests.first()
        self.stdout.write(f"\n📝 Sample UserRequest:")
        self.stdout.write(f"  - Name: {sample_request.name} {sample_request.surname}")
        self.stdout.write(f"  - Email: {sample_request.email}")
        self.stdout.write(f"  - Phone: {sample_request.phone}")
        self.stdout.write(f"  - Profession: {sample_request.profession}")
        self.stdout.write(f"  - Lodge: {sample_request.lodge_name} #{sample_request.lodge_number}")
        self.stdout.write(f"  - Approved: {sample_request.approved}")
        
        # Test user creation logic
        self.stdout.write(f"\n🔧 Testing user creation logic:")
        
        try:
            # Simulate user creation
            user = CustomUser.objects.create_user(
                username=sample_request.email,
                email=sample_request.email,
                password='test_password_123',
                first_name=sample_request.name,
                last_name=sample_request.surname,
                phone_number=sample_request.phone,
                profession=sample_request.profession,
                is_staff=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ User created successfully: {user.email}")
            )
            
            # Try to find and associate the lodge
            try:
                lodge = Lodge.objects.get(number=sample_request.lodge_number)
                self.stdout.write(f"✅ Lodge found: {lodge.name}")
                
                # Create UserLodge association
                user_lodge = UserLodge.objects.create(
                    user=user,
                    lodge=lodge
                )
                self.stdout.write(f"✅ UserLodge association created: {user_lodge}")
                
            except Lodge.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Lodge with number {sample_request.lodge_number} not found")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error associating user with lodge: {e}")
                )
            
            # Clean up test user
            user.delete()
            self.stdout.write(f"🧹 Test user cleaned up")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating test user: {e}")
            )
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS("🎉 User creation test completed!")
        )
