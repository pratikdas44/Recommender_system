from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Teacher(models.Model):
    TEACHER_NAME = models.CharField(max_length=200)
    def __str__(self):
        return self.TEACHER_NAME

class TeacherFeedback(models.Model):
    TIMESTAMP = models.DateTimeField(auto_now_add=True)
    STUDENT_NAME = models.CharField(max_length=200)
    COLLEGE_NAME = models.CharField(max_length=200)
    PREVIOUS_CLASS_MARKS= models.FloatField('PREVIOUS MARKS (IN PERCENTAGE)', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    MEDIUM = models.CharField(max_length=200, choices=(("English","English") , ("Hindi", "Hindi")))
    PREFERED_WAY_OF = models.CharField('PREFERED SUBJECT TYPE', max_length=200, choices=(("Theoritical", "Theoritical"), ("Practical","Practical"), ("Numerical","Numerical")))
    STUDY_HOURS_DAILY= models.FloatField('Study Hours Daily', validators=[MinValueValidator(0), MaxValueValidator(24)], null=True, blank=True)
    TEACHERS_YOU_LIKED = models.ManyToManyField(Teacher,  related_name='LIKED')
    TEACHERS_YOU_DISLIKED = models.ManyToManyField(Teacher, related_name='DISLIKED')
    # TEACHERS_YOU_LIKED = models.ManyToManyField(Teacher,  related_name='LIKED')
    # TEACHERS_YOU_DISLIKED = models.ManyToManyField(Teacher, related_name='DISLIKED')
    def __str__(self):
        return self.STUDENT_NAME

    def to_dict(self):
        return {
            'TIMESTAMP':self.TIMESTAMP,
            'STUDENT_NAME':self.STUDENT_NAME,
            'SUBJECT_NAME':self.SUBJECT_NAME,
            # 'TOUGHNESS_LEVEL':self.TOUGHNESS_LEVEL,
            # 'TYPE_OF':self.TYPE_OF,
            # 'SUBJECT_SYLLABUS':self.SUBJECT_SYLLABUS,
            # 'PREFERRED_READING':self.PREFERRED_READING,
            # 'INTEREST_LEVEL':self.INTEREST_LEVEL,
            # 'SUPPORTING_KNOWLEDGE':self.SUPPORTING_KNOWLEDGE,
            # 'AVERAGE_READING':self.AVERAGE_READING,
            # 'CURRENT_STATUS':self.CURRENT_STATUS,
            # 'NUMBER_OF':self.NUMBER_OF,
            # 'DUE_DATE':self.DUE_DATE,
            # 'DESIRED_NUMBER':self.DESIRED_NUMBER,
            # 'CHECKING_LEVEL':self.CHECKING_LEVEL,
            # 'MARKS_IN':self.MARKS_IN,
            # 'EDUCATION_TYPE':self.EDUCATION_TYPE,
            # 'SEMESTER':self.SEMESTER,
            # 'AS_PER':self.AS_PER,
            # 'PRED_HOUR': self.PRED_HOUR,
        }