from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Complaint(models.Model):
    SERVICE_CHOICES = [
        ('Call Drop', 'Call Drop'),
        ('Slow Internet', 'Slow Internet'),
        ('SMS Failure', 'SMS Failure'),
        ('No Network', 'No Network'),
    ]

    # Link to user, allow null for old records
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    description = models.TextField()
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    location_area = models.CharField(max_length=100, null=True, blank=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"


class EmailVerification(models.Model):
    """Stores OTP for email verification (two-step account protection)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    # NOT auto_now_add so we can reset it when resending OTP
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        """Returns True if OTP is older than 10 minutes."""
        return (timezone.now() - self.created_at).total_seconds() > 600

    def __str__(self):
        return f"{self.user.username} — {'Verified' if self.is_verified else 'Pending'}"


class PasswordResetOTP(models.Model):
    """Stores OTP for forgot password flow."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        """Returns True if OTP is older than 10 minutes."""
        return (timezone.now() - self.created_at).total_seconds() > 600

    def __str__(self):
        return f"Reset OTP for {self.user.username}"
