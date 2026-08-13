from django.contrib import admin
from django.urls import path, include
from django.urls import path
from telecomcomplaints.admin import admin_site


urlpatterns = [
    
    path('admin/', admin_site.urls),
    path('', include('telecomcomplaints.urls')),  # ✅ This line connects your app's urls
    
]
