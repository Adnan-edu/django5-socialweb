from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image

# Create your views here.

@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # Assign current user to the item
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            # Redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # Build the form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        'images/image/create.html',
        {
            'section': 'images',
            'form': form
        }
    )

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request,
        'images/image/detail.html',
        {'section': 'images', 'image': image},
    )