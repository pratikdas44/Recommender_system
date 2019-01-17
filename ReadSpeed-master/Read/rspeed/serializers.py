from rest_framework import serializers
from rspeed.models import ReadSpeed

class ReadSpeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadSpeed
        fields = ('STUDENT_NAME' ,'SUBJECT_NAME', 'TOUGHNESS_LEVEL', 'TYPE_OF', 'SUBJECT_SYLLABUS',
        'PREFERRED_READING', 'INTEREST_LEVEL', 'SUPPORTING_KNOWLEDGE',
        'AVERAGE_READING', 'CURRENT_STATUS', 'NUMBER_OF', 'DESIRED_NUMBER',
        'CHECKING_LEVEL', 'MARKS_IN', 'AS_PER')