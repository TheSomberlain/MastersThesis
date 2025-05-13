import time
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ImagesForm
from .forms import SimpleRegisterForm
from .models import ProcessedImage
from model_utils import process_with_yolo
from django.views.decorators.csrf import csrf_exempt
from WebServer import settings
import os
import uuid

UPLOAD_DIR = 'media/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@login_required
def upload_images(request):
    form = ImagesForm()
    return render(request, 'detector/upload.html', {'form': form})

@login_required
def view_history(request):
    records = ProcessedImage.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'detector/history.html', {'records': records})

def home_page(request):
    return render(request, 'detector/home.html')

def register(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SimpleRegisterForm()
        print(form)
    return render(request, 'detector/signup.html', {'form': form})

def result_view(request, image_id):
    result_images = request.session.get('result_images', [])
    print(result_images)
    total_images = len(result_images)

    if total_images == 0 or image_id < 1 or image_id > total_images:
        return render(request, 'error.html', {'message': 'No analysis results yet.'})

    current_image = result_images[image_id - 1]

    context = {
        'current_image': current_image,
        'current_id': image_id,
        'total_images': total_images
    }
    return render(request, 'detector/result.html', context)

@csrf_exempt
def upload_files_api(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        saved_files = []
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            saved_files.append(file.name)
        return JsonResponse({'status': 'success', 'files': saved_files})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def start_analysis_api(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        if not uploaded_files:
            return JsonResponse({'status': 'error', 'message': 'No files provided.'}, status=400)

        result_images = []
        output_dir = os.path.join(settings.MEDIA_ROOT, 'results')
        os.makedirs(output_dir, exist_ok=True)
        rois = []
        for uploaded_file in uploaded_files:
            try:

                temp_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
                temp_path = os.path.join(output_dir, temp_filename)
                with open(temp_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                output_image, df, regions = process_with_yolo(temp_path)
                result_filename = f"result_{uuid.uuid4().hex}.png"
                result_path = os.path.join(output_dir, result_filename)
                output_image.save(result_path)

                result_images.append(f'/media/results/{result_filename}')

                os.remove(temp_path)
            except Exception as e:
                print(f"[ERROR] Failed to process uploaded file: {e}")

        request.session['result_images'] = result_images
        return JsonResponse({
            'status': 'completed',
            'redirect': '/result/1/',
            'images': result_images
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
