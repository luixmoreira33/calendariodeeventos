"""
Django management command to simulate UserRequest approval.

Usage:
    python manage.py simulate_user_approval [--email EMAIL]
"""

from django.core.management.base import BaseCommand
from calendarrequest.models import UserRequest
from accounts.models import CustomUser, UserLodge
from lodge.models import Lodge
from setup.models import Setup


class Command(BaseCommand):
    help = 'Simulate UserRequest approval process'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email of the UserRequest to approve'
        )

    def handle(self, *args, **options):
        self.stdout.write("🔧 SIMULATING USERREQUEST APPROVAL")
        self.stdout.write("="*50)
        
        # Check Setup configuration
        setup = Setup.objects.last()
        if not setup:
            self.stdout.write(
                self.style.ERROR("❌ No Setup configuration found!")
            )
            return
        
        self.stdout.write(f"✅ Setup found: {setup.url}")
        
        # Find UserRequest to approve
        if options['email']:
            try:
                user_request = UserRequest.objects.get(email=options['email'])
            except UserRequest.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"❌ UserRequest with email {options['email']} not found!")
                )
                return
        else:
            # Get first unapproved UserRequest
            user_request = UserRequest.objects.filter(approved=False).first()
            if not user_request:
                self.stdout.write(
                    self.style.WARNING("⚠️  No unapproved UserRequest found!")
                )
                return
        
        self.stdout.write(f"📝 UserRequest to approve:")
        self.stdout.write(f"  - Name: {user_request.name} {user_request.surname}")
        self.stdout.write(f"  - Email: {user_request.email}")
        self.stdout.write(f"  - Phone: {user_request.phone}")
        self.stdout.write(f"  - Profession: {user_request.profession}")
        self.stdout.write(f"  - Lodge: {user_request.lodge_name} #{user_request.lodge_number}")
        self.stdout.write(f"  - Approved: {user_request.approved}")
        
        # Check if user already exists
        if CustomUser.objects.filter(email=user_request.email).exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️  User with email {user_request.email} already exists!")
            )
            return
        
        # Check if lodge exists
        try:
            lodge = Lodge.objects.get(number=user_request.lodge_number)
            self.stdout.write(f"✅ Lodge found: {lodge.name}")
        except Lodge.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"⚠️  Lodge with number {user_request.lodge_number} not found")
            )
            lodge = None
        
        # Simulate approval
        self.stdout.write(f"\n🔧 Simulating approval process:")
        
        try:
            # Create user
            user = CustomUser.objects.create_user(
                username=user_request.email,
                email=user_request.email,
                password='temp_password_123',
                first_name=user_request.name,
                last_name=user_request.surname,
                phone_number=user_request.phone,
                profession=user_request.profession,
                is_staff=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ User created successfully: {user.email}")
            )
            
            # Associate with lodge if found
            if lodge:
                try:
                    user_lodge = UserLodge.objects.create(
                        user=user,
                        lodge=lodge
                    )
                    self.stdout.write(f"✅ UserLodge association created: {user_lodge}")
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Error creating UserLodge: {e}")
                    )
            
            # Mark UserRequest as approved
            user_request.approved = True
            user_request.save()
            self.stdout.write(f"✅ UserRequest marked as approved")
            
            self.stdout.write(f"\n🎉 Approval simulation completed successfully!")
            self.stdout.write(f"  - User: {user.email}")
            self.stdout.write(f"  - Password: temp_password_123")
            self.stdout.write(f"  - Lodge: {lodge.name if lodge else 'None'}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error during approval simulation: {e}")
            )
            # Clean up if user was created
            if 'user' in locals():
                try:
                    user.delete()
                    self.stdout.write(f"🧹 Cleaned up created user due to error")
                except:
                    pass
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS("🎉 UserRequest approval simulation completed!")
        )
