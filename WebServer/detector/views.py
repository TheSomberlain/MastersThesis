from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ImagesForm
from .forms import SimpleRegisterForm
from .models import ProcessedImage
from .models import Reports

def upload_images(request):
    form = ImagesForm()
    return render(request, 'detector/upload.html', {'form': form})

@login_required
def report_view(request, report_id):
    report = Reports.objects.get(id=report_id, user=request.user)
    return render(request, 'detector/report_view.html', {'report': report})

@login_required
def history_view(request):
    reports = Reports.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'detector/history.html', {'reports': reports})
    
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
    image_ids = request.session.get('last_image_ids', [image_id])

    images = ProcessedImage.objects.filter(id__in=image_ids)

    images_with_rois = []
    for img in images:
        rois = img.rois.all()
        images_with_rois.append({
            'id': img.id,
            'url': img.image_file.url,
            'uploaded_at': img.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'rois': [
                {
                    'id': roi.id,
                    'url': roi.roi_file.url,
                    'label': roi.label
                }
                for roi in rois
            ]
        })

    current_image_dict = next((img for img in images_with_rois if img['id'] == image_id), None)
    if not current_image_dict:
        return render(request, 'detector/error.html', {'message': 'Image not found.'})

    context = {
        'current_image': current_image_dict,
        'images_with_rois': images_with_rois,
        'image_ids': image_ids,
        'current_id': image_id,
        'current_pos': image_id - min(image_ids) + 1,
        'total_images': len(image_ids)
    }
    return render(request, 'detector/result.html', context)