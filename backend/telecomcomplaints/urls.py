from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('success/', views.complaint_success, name='complaint_success'),
    path('complaints/', views.view_complaints, name='view_complaints'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    # Email verification
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    # Forgot / Reset password
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    # Home root
    path('', views.home_view, name='home'),
]
