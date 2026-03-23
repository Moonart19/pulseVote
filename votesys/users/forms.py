from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Username'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'Email'
    }))
    bio = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={
        'class': 'form-input', 'placeholder': 'Tell us about yourself...', 'rows': 3
    }))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-input', 'accept': 'image/*'
    }))

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']