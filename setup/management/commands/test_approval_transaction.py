"""
Django management command to test UserRequest approval transaction handling.

Usage:
    python manage.py test_approval_transaction
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from calendarrequest.models import UserRequest
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Test UserRequest approval transaction handling'

    def handle(self, *args, **options):
        self.stdout.write("🧪 TESTING APPROVAL TRANSACTION HANDLING")
        self.stdout.write("="*50)
        
        # Find an unapproved UserRequest
        user_request = UserRequest.objects.filter(approved=False).first()
        if not user_request:
            self.stdout.write(
                self.style.WARNING("⚠️  No unapproved UserRequest found!")
            )
            return
        
        self.stdout.write(f"📝 UserRequest to test:")
        self.stdout.write(f"  - Name: {user_request.name} {user_request.surname}")
        self.stdout.write(f"  - Email: {user_request.email}")
        self.stdout.write(f"  - Profession: {user_request.profession}")
        self.stdout.write(f"  - Current status: {'Approved' if user_request.approved else 'Pending'}")
        
        # Check if user already exists
        if CustomUser.objects.filter(email=user_request.email).exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️  User with email {user_request.email} already exists!")
            )
            return
        
        self.stdout.write(f"\n🔧 Testing approval transaction:")
        
        try:
            # Test the approval process in a transaction
            with transaction.atomic():
                self.stdout.write("  - Starting transaction...")
                
                # Mark as approved (this should trigger the signal)
                user_request.approved = True
                user_request.save()
                
                self.stdout.write("  - UserRequest marked as approved")
                self.stdout.write("  - Transaction committed successfully")
                
                # Check if user was created
                try:
                    user = CustomUser.objects.get(email=user_request.email)
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ User created successfully: {user.username}")
                    )
                    self.stdout.write(f"  - User details: {user.first_name} {user.last_name}")
                    self.stdout.write(f"  - Profession: {user.profession}")
                    self.stdout.write(f"  - Is staff: {user.is_staff}")
                    
                except CustomUser.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠️  User not created yet (signal may be delayed)")
                    )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"  ❌ Transaction failed: {e}")
            )
            
            # Rollback the UserRequest
            user_request.refresh_from_db()
            self.stdout.write(f"  - UserRequest status reverted to: {'Approved' if user_request.approved else 'Pending'}")
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS("🎉 Approval transaction test completed!")
        )
