from django.shortcuts import render
from .forms import ImageUploadForm
from django.core.files.storage import default_storage
from django.conf import settings
import easyocr
import os

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
