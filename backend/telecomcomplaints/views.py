import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.cache import never_cache

from .forms import ComplaintForm, CustomUserCreationForm, ForgotPasswordForm, ResetPasswordForm
from .models import Complaint, EmailVerification, PasswordResetOTP


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def generate_otp():
    """Generate a random 6-digit OTP code."""
    return str(random.randint(100000, 999999))


def send_verification_email(user, otp_code):
    """Send email verification OTP to the user's email address."""
    send_mail(
        subject='🔐 MTN Portal — Email Verification Code',
        message=(
            f"Hello {user.username},\n\n"
            f"Your email verification code is:\n\n"
            f"  {otp_code}\n\n"
            f"This code expires in 10 minutes.\n"
            f"Do NOT share this code with anyone.\n\n"
            f"This is a two-step security verification to protect your account.\n"
            f"If you did not create this account, please ignore this email.\n\n"
            f"— MTN Complaint & Tracking System\n"
            f"  Nigeria Customer Portal"
        ),
        from_email='MTN Complaint System <abubakarsadeeq3647@gmail.com>',
        recipient_list=[user.email],
        fail_silently=False,
    )


# ─── SIGNUP VIEW ──────────────────────────────────────────────────────────────

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Lock account until email is verified
            user.save()

            # Generate and save OTP
            otp_code = generate_otp()
            ev, _ = EmailVerification.objects.get_or_create(user=user)
            ev.otp_code = otp_code
            ev.is_verified = False
            ev.created_at = timezone.now()
            ev.save()

            # Send verification email
            try:
                send_verification_email(user, otp_code)
                messages.success(
                    request,
                    f"Account created! A 6-digit verification code has been sent to {user.email}. "
                    f"Please check your inbox (and spam folder)."
                )
            except Exception:
                messages.warning(
                    request,
                    "Account created, but the email could not be sent. "
                    "Use the 'Resend OTP' button on the next page."
                )

            request.session['verification_username'] = user.username
            return redirect('verify_email')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


# ─── VERIFY EMAIL VIEW ────────────────────────────────────────────────────────

def verify_email_view(request):
    username = request.session.get('verification_username')
    if not username:
        return redirect('signup')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('signup')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code', '').strip()

        try:
            verification = EmailVerification.objects.get(user=user)
        except EmailVerification.DoesNotExist:
            messages.error(request, "Verification record not found. Please sign up again.")
            return redirect('signup')

        if verification.is_expired():
            messages.error(request, "OTP has expired. Please click 'Resend OTP' to get a new code.")
            return render(request, 'verify_email.html', {'email': user.email})

        if entered_otp == verification.otp_code:
            verification.is_verified = True
            verification.save()
            user.is_active = True
            user.save()
            request.session.pop('verification_username', None)
            messages.success(request, "✅ Email verified successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "❌ Invalid OTP code. Please check your email and try again.")

    return render(request, 'verify_email.html', {'email': user.email})


# ─── RESEND OTP VIEW ──────────────────────────────────────────────────────────

def resend_otp_view(request):
    username = request.session.get('verification_username')
    if not username:
        return redirect('signup')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('signup')

    otp_code = generate_otp()
    ev, _ = EmailVerification.objects.get_or_create(user=user)
    ev.otp_code = otp_code
    ev.is_verified = False
    ev.created_at = timezone.now()
    ev.save()

    try:
        send_verification_email(user, otp_code)
        messages.success(request, f"A new OTP code has been sent to {user.email}.")
    except Exception:
        messages.error(request, "Failed to send email. Please try again.")

    return redirect('verify_email')


# ─── LOGIN VIEW ───────────────────────────────────────────────────────────────

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username', '').strip()

        # Check if user exists but email not verified
        try:
            user_obj = User.objects.get(username=username)
            if not user_obj.is_active:
                request.session['verification_username'] = username
                messages.error(
                    request,
                    "Your email address is not yet verified. "
                    "Please check your inbox for the OTP code."
                )
                return render(request, 'login.html', {'form': form, 'show_verify_link': True})
        except User.DoesNotExist:
            pass

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# ─── LOGOUT VIEW ─────────────────────────────────────────────────────────────

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


# ─── HOME VIEW ────────────────────────────────────────────────────────────────

@never_cache
@login_required
def home_view(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Complaint submitted successfully.")
            return redirect('my_complaints')
    else:
        form = ComplaintForm()

    complaint_count = Complaint.objects.filter(user=request.user).count()
    return render(request, 'home.html', {'form': form, 'complaint_count': complaint_count})


# ─── SUBMIT COMPLAINT VIEW ───────────────────────────────────────────────────

@never_cache
@login_required
def submit_complaint(request):
    if request.method == 'POST':
        name = request.user.get_full_name() or request.user.username
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        service_type = request.POST.get('service_type')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        address = None
        location_area = None
        if latitude and longitude:
            try:
                from geopy.geocoders import Nominatim
                geolocator = Nominatim(user_agent="complaints_app")
                location = geolocator.reverse(f"{latitude}, {longitude}", language="en")
                if location:
                    address = location.address
                    location_area = (
                        location.raw.get("address", {}).get("state")
                        or location.raw.get("address", {}).get("city")
                        or location.raw.get("address", {}).get("town")
                        or "Unknown"
                    )
            except Exception as e:
                print(f"Geocoding error: {e}")

        Complaint.objects.create(
            user=request.user,
            name=name,
            phone_number=phone,
            email=email,
            service_type=service_type,
            description=description,
            latitude=latitude,
            longitude=longitude,
            address=address,
            location_area=location_area,
        )

        messages.success(request, "Your complaint has been submitted successfully.")
        return redirect('thank_you')

    return render(request, 'submit_complaint.html')


# ─── VIEW ALL COMPLAINTS ─────────────────────────────────────────────────────

@login_required
def view_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, 'view_complaints.html', {'complaints': complaints})


# ─── COMPLAINT SUCCESS ────────────────────────────────────────────────────────

def complaint_success(request):
    return render(request, 'complaint_success.html')


# ─── THANK YOU ────────────────────────────────────────────────────────────────

def thank_you(request):
    return render(request, 'thank_you.html')


# ─── MY COMPLAINTS ────────────────────────────────────────────────────────────

@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-submitted_at')
    complaint_count = complaints.count()
    return render(request, 'my_complaints.html', {
        'complaints': complaints,
        'complaint_count': complaint_count,
    })


# ─── FORGOT PASSWORD ──────────────────────────────────────────────────────────

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email__iexact=email)

                # Generate reset OTP
                otp_code = generate_otp()
                PasswordResetOTP.objects.create(user=user, otp_code=otp_code)

                send_mail(
                    subject='🔑 MTN Portal — Password Reset OTP',
                    message=(
                        f"Hello {user.username},\n\n"
                        f"You requested a password reset for your MTN Complaint Portal account.\n\n"
                        f"Your OTP code is:\n\n"
                        f"  {otp_code}\n\n"
                        f"This code expires in 10 minutes.\n"
                        f"If you did not request this, please ignore this email — your account is safe.\n\n"
                        f"— MTN Complaint & Tracking System\n"
                        f"  Nigeria Customer Portal"
                    ),
                    from_email='MTN Complaint System <abubakarsadeeq3647@gmail.com>',
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                request.session['reset_email'] = email
                messages.success(
                    request,
                    f"A password reset OTP has been sent to {email}. "
                    f"Please check your inbox (and spam folder)."
                )
                return redirect('reset_password')

            except User.DoesNotExist:
                messages.error(request, "No account found with that email address.")
            except Exception:
                messages.error(request, "Failed to send reset email. Please try again.")
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})


# ─── RESET PASSWORD ───────────────────────────────────────────────────────────

def reset_password_view(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp_code']
            new_password = form.cleaned_data['new_password']

            try:
                user = User.objects.get(email__iexact=email)
                reset_otp = PasswordResetOTP.objects.filter(
                    user=user, is_used=False
                ).order_by('-created_at').first()

                if not reset_otp:
                    messages.error(request, "No OTP found. Please request a new one.")
                    return redirect('forgot_password')

                if reset_otp.is_expired():
                    messages.error(request, "OTP has expired. Please request a new one.")
                    return redirect('forgot_password')

                if entered_otp == reset_otp.otp_code:
                    user.set_password(new_password)
                    user.save()
                    reset_otp.is_used = True
                    reset_otp.save()
                    request.session.pop('reset_email', None)
                    messages.success(
                        request,
                        "✅ Password reset successful! Please log in with your new password."
                    )
                    return redirect('login')
                else:
                    messages.error(request, "❌ Invalid OTP code. Please check and try again.")

            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('forgot_password')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form, 'email': email})
