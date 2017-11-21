from django.db import models
import datetime
from django.utils.timezone import now
from brain.models import StudentRoster

class Assessment(models.Model):
    student = models.ForeignKey(StudentRoster,)
    date_given = models.DateField(default=now)

    class Meta:
        abstract = True

class NWEA(Assessment):
    math_rit = models.IntegerField()
    math_percentile = models.IntegerField()
    reading_rit = models.IntegerField()
    reading_percentile = models.IntegerField()
    reading_lexile = models.CharField(max_length=50)

class DRA(Assessment):
    level_letter = models.CharField(max_length=10,)
    level_number = models.IntegerField()
    myon_lexile = models.IntegerField(null=True, blank=True)

class CBA(Assessment):
    cba_percentage = models.IntegerField()
    performance_task = models.IntegerField()
    addition_facts = models.IntegerField(null=True, blank=True)
    subtraction_facts = models.IntegerField(null=True, blank=True)
    multiplication_facts = models.IntegerField(null=True, blank=True)
    division_facts = models.IntegerField(null=True, blank=True)

class Writing(Assessment):
    WRITING_TYPES = [("Informational", "Informational"), ("Narrative", "Narrative"),
                     ("Persuasive", "Persuasive"), ]
    PRE_OR_POST = [("Pre", "Pre"), ("Post", "Post"), ]
    teacher_score = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    blind_score = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    total_score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, )
    type = models.CharField(choices=WRITING_TYPES, max_length=55)
    pre_or_post = models.CharField(choices=PRE_OR_POST, max_length=55)

class ENI(Assessment):
    counting = models.IntegerField()
    place_value = models.IntegerField()
    add_sub = models.IntegerField()
    mult_div = models.IntegerField()
    total = models.IntegerField()

class CoreKnowledge(Assessment):
    assessment_name = models.CharField(max_length=255,)
    da1 = models.IntegerField(blank=True, null=True,)
    da2 = models.IntegerField(blank=True, null=True,)
    da3 = models.IntegerField(blank=True, null=True,)
    da4 = models.IntegerField(blank=True, null=True,)
    da5 = models.IntegerField(blank=True, null=True,)


class ELAPBA(Assessment):
    assessment_name = models.CharField(max_length=255,)
    score = models.DecimalField(max_digits=3, decimal_places=1)


class Investigations(Assessment):
    assessment_name = models.CharField(max_length=255,)
    score = models.IntegerField()

