from django import forms
from .models import Image
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }
    # Implement 'url' field validation
    def clean_url(self):
        url = self.cleaned_data['url'] # Value of the url field is retrieved
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not match valid image extensions.'
            )
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False) # A new image instance is created
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # Download image from given url
        response = requests.get(image_url)
        image.image.save(
            image_name,
            ContentFile(response.content),  # File is saved to the media directory of the project
            save=False  # Prevent the object from being saved to the database
        )
        if commit:
            image.save()
        return image