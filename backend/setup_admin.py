import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

print("=== ACCOUNTS IN DATABASE ===")
users = User.objects.all()
for u in users:
    print(f"  Username: {u.username} | Email: {u.email} | Admin: {u.is_superuser}")
print(f"Total: {users.count()} account(s)")
print("")

# Create superuser if none exists
if not User.objects.filter(is_superuser=True).exists():
    print("No admin found. Creating superuser...")
    User.objects.create_superuser(
        username='admin',
        email='admin@mtn.com',
        password='Admin1234'
    )
    print("Superuser created!")
    print("  Username: admin")
    print("  Password: Admin1234")
else:
    admins = User.objects.filter(is_superuser=True)
    print("Admin account(s) already exist:")
    for a in admins:
        print(f"  Username: {a.username} | Email: {a.email}")

print("")
print("DONE")
