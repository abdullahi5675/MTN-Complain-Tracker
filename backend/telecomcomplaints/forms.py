from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        """Enforce one email per account — no duplicate emails allowed."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists. Please use a different email."
            )
        return email


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'email', 'service_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Registered Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your registered email address',
            'style': 'width:100%; padding:12px; border:1px solid #ccc; border-radius:8px; font-size:15px;'
        })
    )


class ResetPasswordForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        label='OTP Code',
        widget=forms.TextInput(attrs={
            'placeholder': '000000',
            'maxlength': '6',
            'inputmode': 'numeric',
            'autocomplete': 'off',
            'style': 'width:100%; padding:12px; font-size:24px; text-align:center; letter-spacing:10px; border:2px solid #ccc; border-radius:8px;'
        })
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter new password',
            'style': 'width:100%; padding:12px; border:1px solid #ccc; border-radius:8px; font-size:15px;'
        })
    )
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your new password',
            'style': 'width:100%; padding:12px; border:1px solid #ccc; border-radius:8px; font-size:15px;'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please try again.")
        return cleaned_data
