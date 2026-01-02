from django import forms
from .models import Complaint, Application


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['room_type', 'occupancy']
