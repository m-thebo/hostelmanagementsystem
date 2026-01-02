from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    semester = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2' , 'name', 'email', 'semester')
