from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.decorators import login_required
import easyocr
import os

@login_required(login_url='login-url')
def ocr_view(request):
    text = None
    uploaded_image_url = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            # Save image using Django's default storage
            file_path = default_storage.save(os.path.join('uploads', image.name), image)
            image_path = os.path.join(settings.MEDIA_ROOT, file_path)
            uploaded_image_url = default_storage.url(file_path)
            try:
                reader = easyocr.Reader(['en'], gpu=False)
                results = reader.readtext(image_path)
                text = "\n".join([res[1] for res in results]) if results else "No text found."
            except Exception as e:
                text = f"Error during OCR: {str(e)}"
    else:
        form = ImageUploadForm()
    return render(request, 'easyocr_app/ocr.html', {
        'form': form,
        'text': text,
        'uploaded_image_url': uploaded_image_url
    })

@login_required(login_url='login-url')
def about(request):
    return render(request, 'easyocr_app/about.html')




def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ocr')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'account/signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)  
                messages.success(request, f'Welcome, {username} ')
                return redirect('ocr')
            else:
                pass
        else:
            pass
    else:
        form = CustomLoginForm()
        
    return render(request, 'account/login.html', {'form': form})
    
def logout_user(request):
    logout(request)
    return redirect('login-url')