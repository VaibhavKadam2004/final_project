from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentProfile

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['tenth_percent', 'twelfth_percent', 'cgpa', 'active_backlogs', 'skills', 'resume']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comma-separated skills'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].help_text = 'Upload PDF/DOC resume for auto skill extraction'
