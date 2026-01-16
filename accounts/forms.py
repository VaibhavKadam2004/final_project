from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentProfile

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role_type = CustomUser.STUDENT
        if commit:
            user.save()
            StudentProfile.objects.create(user=user)
        return user
