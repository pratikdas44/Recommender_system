from rest_framework import serializers
from tutor.models import TeacherFeedback, Teacher

class TeacherFeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeacherFeedback
        fields = ('STUDENT_NAME' ,'COLLEGE_NAME', 'PREVIOUS_CLASS_MARKS', 'MEDIUM', 'PREFERED_WAY_OF',
        'STUDY_HOURS_DAILY', 'TEACHERS_YOU_LIKED', 'TEACHERS_YOU_DISLIKED')
class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = ('TEACHER_NAME',)
