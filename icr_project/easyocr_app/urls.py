from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login-url'),  # Changed to redirect to login page first
    path('ocr/', views.ocr_view, name='ocr'),  # Moved OCR to its own path
    path('signup/', views.signup, name='signup-url'),
    path('about/', views.about, name='about-url')
]