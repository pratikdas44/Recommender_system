from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ReadSpeed(models.Model):
    TIMESTAMP = models.DateTimeField(auto_now_add=True)
    STUDENT_NAME = models.CharField(max_length=200)
    SUBJECT_NAME = models.CharField(max_length=200)
    TOUGHNESS_LEVEL = models.CharField(max_length=200, choices=(("Easy","Easy") , ("Medium", "Medium"), ("Hard", "Hard")))
    TYPE_OF = models.CharField('TYPE OF SUBJECT', max_length=200, choices=(("Theoritical", "Theoritical"), ("Practical","Practical"), ("Numerical","Numerical") , ("Other","Other")))
    SUBJECT_SYLLABUS = models.CharField(max_length=200, choices=(("Very Lengthy (800+ pages)","Very Lengthy (800+ pages)"), ("Lengthy (600+ pages)", "Lengthy (600+ pages)"), ("Medium (400+ pages)","Medium (400+ pages)"), ("Short", "Short") ))
    PREFERRED_READING= models.CharField(max_length=200, choices=(("Notes","Notes"), ("Book", "Book"), ("Video","Video"), ("Multiple","Multiple")))
    INTEREST_LEVEL= models.CharField(max_length=200, choices=(("Very Interesting","Very Interesting"), ("Interesting", "Interesting"), ("Normal","Normal"), ("Boring","Boring")))
    SUPPORTING_KNOWLEDGE= models.CharField(max_length=200, choices=(("None","None"), ("Beginner", "Beginner"), ("Intermediate","Intermediate"), ("Expert","Expert")))
    AVERAGE_READING = models.FloatField('AVG TIME READING PER PAGE (IN MINS)', default=1, validators=[MinValueValidator(1), MaxValueValidator(30)])
    CURRENT_STATUS = models.IntegerField(default=0,  choices=((0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)))
    NUMBER_OF = models.IntegerField('NO OF REVISION', default=0,  choices=((0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)))
    DUE_DATE =  models.DateTimeField(auto_now_add=True, blank=True)
    DESIRED_NUMBER = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    CHECKING_LEVEL= models.CharField(max_length=200, choices=(("Strict","Strict"), ("Normal", "Normal"), ("Lenient","Lenient")))
    MARKS_IN= models.FloatField('MARKS IN SIMILAR SUBJECT', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    EDUCATION_TYPE= models.CharField(default='Graduation', max_length=200, choices=(("School","School"), ("Graduation", "Graduation"), ("Post Graduation","Post Graduation")))
    SEMESTER= models.FloatField(default=1, validators=[MinValueValidator(1), MaxValueValidator(12)])
    AS_PER= models.FloatField('NO OF HOURS REQUIRED AS PER YOU', validators=[MinValueValidator(0), MaxValueValidator(200)])
    def __str__(self):
        return self.STUDENT_NAME
    def to_dict(self):
        return {
            'TIMESTAMP':self.TIMESTAMP,
            'STUDENT_NAME':self.STUDENT_NAME,
            'SUBJECT_NAME':self.SUBJECT_NAME,
            'TOUGHNESS_LEVEL':self.TOUGHNESS_LEVEL,
            'TYPE_OF':self.TYPE_OF,
            'SUBJECT_SYLLABUS':self.SUBJECT_SYLLABUS,
            'PREFERRED_READING':self.PREFERRED_READING,
            'INTEREST_LEVEL':self.INTEREST_LEVEL,
            'SUPPORTING_KNOWLEDGE':self.SUPPORTING_KNOWLEDGE,
            'AVERAGE_READING':self.AVERAGE_READING,
            'CURRENT_STATUS':self.CURRENT_STATUS,
            'NUMBER_OF':self.NUMBER_OF,
            'DUE_DATE':self.DUE_DATE,
            'DESIRED_NUMBER':self.DESIRED_NUMBER,
            'CHECKING_LEVEL':self.CHECKING_LEVEL,
            'MARKS_IN':self.MARKS_IN,
            'EDUCATION_TYPE':self.EDUCATION_TYPE,
            'SEMESTER':self.SEMESTER,
            'AS_PER':self.AS_PER,
        }