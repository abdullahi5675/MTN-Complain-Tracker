import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Create a fresh clean admin account
if User.objects.filter(username='mtn_admin').exists():
    User.objects.filter(username='mtn_admin').delete()

admin = User.objects.create_superuser(
    username='mtn_admin',
    email='admin@mtn.com',
    password='MTN@2026'
)
print(f"ADMIN CREATED: username=mtn_admin | password=MTN@2026")

# Reset password for a regular user account so you can test it
user = User.objects.filter(username='Abdullahi_H_Nayaya').first()
if user:
    user.set_password('User@2026')
    user.save()
    print(f"USER PASSWORD RESET: username=Abdullahi_H_Nayaya | password=User@2026")

print("")
print("ALL DONE - you can now log in!")
