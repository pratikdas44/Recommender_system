from django import forms
from rspeed.models import ReadSpeed
from django.urls.base import reverse_lazy

class ReadSpeedForm(forms.ModelForm):
    # STUDENT_NAME = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Student Name'}))
    # phone_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone No'}))
    # email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'EMail'}))
    class Meta:
        model = ReadSpeed
        fields = ['STUDENT_NAME' ,'SUBJECT_NAME', 'TOUGHNESS_LEVEL', 'TYPE_OF', 'SUBJECT_SYLLABUS',
        'PREFERRED_READING', 'INTEREST_LEVEL', 'SUPPORTING_KNOWLEDGE',
        'AVERAGE_READING', 'CURRENT_STATUS', 'NUMBER_OF', 'DESIRED_NUMBER',
        'CHECKING_LEVEL', 'MARKS_IN', 'AS_PER']

#         fields = ['skills', 'phone_no', 'email', 'myimg']
