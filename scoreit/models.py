from django.db import models
from django.core.urlresolvers import reverse
import datetime
from django.utils.timezone import now
# Create your models here.
from brain.models import Subject, StudentRoster, Classroom, CurrentClass

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class Score(models.Model):
    student = models.ForeignKey(StudentRoster)
    subject = models.ForeignKey(Subject)
    date = models.DateField(default=now, verbose_name="Date")
    hand = models.BooleanField(default=False, verbose_name="Raised Hand", choices=BOOL_CHOICES)
    slant = models.BooleanField(default=False, verbose_name="SLANT", choices=BOOL_CHOICES)
    transition = models.BooleanField(default=False, verbose_name="Transitions", choices=BOOL_CHOICES)
    please = models.BooleanField(default=False, verbose_name="Please/Thank You", choices=BOOL_CHOICES)
    instruction = models.BooleanField(default=False, verbose_name="Instructions 1st Time", choices=BOOL_CHOICES)
    material = models.BooleanField(default=False, verbose_name="Respected Materials", choices=BOOL_CHOICES)
    peer = models.BooleanField(default=False, verbose_name="Respected Peers", choices=BOOL_CHOICES)

    def get_absolute_url(self):
        return reverse('scoreit:classlist', kwargs={
            'student_id': self.student.student_id,
        })

    def __str__(self):
        return "{} {} {}".format(self.student, self.subject, self.date)


class TeacherApproval(models.Model):
    APPROVAL_CHOICES = (("YES","YES"),("NO","NO"))
    student = models.ForeignKey(StudentRoster)
    date = models.DateField(default=now, verbose_name='Date')
    approved = models.CharField(max_length=100, default="NO")

    class Meta:
        verbose_name = 'Teacher Approval'
        verbose_name_plural = 'Teacher Approvals'