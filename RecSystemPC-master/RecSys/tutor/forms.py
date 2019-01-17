from django import forms
from tutor.models import TeacherFeedback
from django.urls.base import reverse_lazy

class TeacherFeedbackForm(forms.ModelForm):
    # MARKS_IN = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Marks in same or similar subject'}))
    # phone_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone No'}))
    # email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'EMail'}))
    class Meta:
        model = TeacherFeedback
        fields = ['STUDENT_NAME' ,'COLLEGE_NAME', 'PREVIOUS_CLASS_MARKS', 'MEDIUM', 'PREFERED_WAY_OF',
        'STUDY_HOURS_DAILY', 'TEACHERS_YOU_LIKED', 'TEACHERS_YOU_DISLIKED']
#         fields = ['skills', 'phone_no', 'email', 'myimg']
