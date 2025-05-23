from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Image

def gallery_view(request):
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    images = Image.objects.filter(created_date__gte=thirty_days_ago).order_by('-created_date')
    return render(request, 'gallery.html', {'images': images})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'image_detail.html', {'image': image})
