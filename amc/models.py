import datetime

from django.db import models

from brain.models import StudentRoster, CurrentClass
# Create your models here.


class AMCTest(models.Model):
    test_number = models.IntegerField(unique=True)
    topic = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    grade_equivalent = models.CharField(max_length=100)
    total_questions = models.IntegerField(default=20)
    minimum_passing_grade = models.IntegerField(default=18)

    def __str__(self):
        return '%s -- %s' % (self.topic, self.name)

    class Meta:
        verbose_name = "AMC Test"
        verbose_name_plural = "AMC Tests"


class AMCTestResult(models.Model):
    student = models.ForeignKey(StudentRoster, blank=False, null=False)
    test = models.ForeignKey(AMCTest)
    score = models.IntegerField(blank=False, null=False)
    date_tested = models.DateField(default=datetime.date.today, verbose_name='Date Tested')

    def passing_score(self):
        if self.score >= self.test.minimum_passing_grade:
            return True
        elif self.score < self.test.minimum_passing_grade:
            return False
        else:
            raise ValueError

    passing_score.boolean = True
    passing_score.short_description = 'Pass?'


    def __str__(self):
        return '%s -- %s Pass: %s' % (self.student, self.test, self.passing_score(), )

    class Meta:
        verbose_name = "AMC Test Score"
        verbose_name_plural = "AMC Test Scores"
        ordering = ['-date_tested', 'student']
        unique_together = ("student", "test", "date_tested")


class AMCStartingTest(models.Model):
    student = models.ForeignKey(StudentRoster, blank=False, null=False)
    starting_test = models.IntegerField(verbose_name='Starting Test')

    class Meta:
        verbose_name = "AMC Starting Test"
        verbose_name_plural = "AMC Starting Tests"