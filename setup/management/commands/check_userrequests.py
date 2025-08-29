"""
Django management command to check UserRequest status.

Usage:
    python manage.py check_userrequests
"""

from django.core.management.base import BaseCommand
from calendarrequest.models import UserRequest
from accounts.models import CustomUser, UserLodge
from lodge.models import Lodge


class Command(BaseCommand):
    help = 'Check UserRequest status and associated users'

    def handle(self, *args, **options):
        self.stdout.write("📋 CHECKING USERREQUEST STATUS")
        self.stdout.write("="*50)
        
        # Check all UserRequests
        user_requests = UserRequest.objects.all().order_by('created_at')
        
        if not user_requests.exists():
            self.stdout.write("⚠️  No UserRequests found.")
            return
        
        self.stdout.write(f"📊 Found {user_requests.count()} UserRequest(s):")
        
        for i, request in enumerate(user_requests, 1):
            self.stdout.write(f"\n{i}. {request.name} {request.surname}")
            self.stdout.write(f"   📧 Email: {request.email}")
            self.stdout.write(f"   📱 Phone: {request.phone}")
            self.stdout.write(f"   💼 Profession: {request.profession}")
            self.stdout.write(f"   🏠 Lodge: {request.lodge_name} #{request.lodge_number}")
            self.stdout.write(f"   ✅ Approved: {request.approved}")
            self.stdout.write(f"   📅 Created: {request.created_at.strftime('%d/%m/%Y %H:%M')}")
            
            # Check if user exists
            try:
                user = CustomUser.objects.get(email=request.email)
                self.stdout.write(f"   👤 User exists: ✅ {user.username}")
                self.stdout.write(f"   🔐 Is staff: {user.is_staff}")
                self.stdout.write(f"   💼 User profession: {user.profession}")
                
                # Check UserLodge associations
                user_lodges = UserLodge.objects.filter(user=user)
                if user_lodges.exists():
                    self.stdout.write(f"   🏠 Associated lodges:")
                    for ul in user_lodges:
                        self.stdout.write(f"      - {ul.lodge.name} ({ul.lodge.number})")
                else:
                    self.stdout.write(f"   🏠 Associated lodges: None")
                    
            except CustomUser.DoesNotExist:
                self.stdout.write(f"   👤 User exists: ❌ Not created yet")
        
        # Summary
        approved_count = user_requests.filter(approved=True).count()
        pending_count = user_requests.filter(approved=False).count()
        
        self.stdout.write(f"\n" + "="*50)
        self.stdout.write("📊 SUMMARY")
        self.stdout.write("="*50)
        self.stdout.write(f"✅ Approved: {approved_count}")
        self.stdout.write(f"⏳ Pending: {pending_count}")
        self.stdout.write(f"📋 Total: {user_requests.count()}")
        
        self.stdout.write(
            self.style.SUCCESS("\n🎉 UserRequest status check completed!")
        )
