from django.db import models
from brain.models import StudentRoster


# Create your models here.

class CGI(models.Model):
    cgi_number = models.IntegerField(unique=True, verbose_name="CGI #")
    name = models.CharField(max_length=50, unique=True, verbose_name="Character Name", help_text="Name of the first person mentioned in the problem.")
    question = models.TextField(max_length=500, unique=True, verbose_name="Problem", help_text="Substitute __ for the numbers in the problem.")
    first_num_original = models.IntegerField(verbose_name="Original Problem's First Number", null=True)
    second_num_original = models.IntegerField(verbose_name="Original Problem's Second Number", null=True)
    first_num_low = models.IntegerField(verbose_name="Minimum for First Number")
    first_num_high = models.IntegerField(verbose_name="Maximum for First Number")
    second_num_low = models.IntegerField(verbose_name="Minimum for Second Number")
    second_num_high = models.IntegerField(verbose_name="Maximum for Second Number")
    gr2_unit = models.IntegerField(verbose_name="Grade 2 Unit", help_text="The Unit in the Grade 2 Scope and Sequence which the CGI is introduced",
                                    blank=True, null=True)
    date_assigned = models.DateField(blank=True, null=True, verbose_name="Date Assigned", help_text="Date the CGI was/will be given to the class.")


    def __str__(self):
        return 'CGI {} - The {} Problem'.format(self.cgi_number, self.name)

    class Meta:
        verbose_name = "CGI Question"
        verbose_name_plural = "CGI Questions"
        ordering = ['cgi_number']

class CGIResult(models.Model):
    CHOICES = [('-', '-'),('0', '0'),('1', '1'),('2', '2'),('3', 'M') ]
    student = models.ForeignKey(StudentRoster,)
    cgi = models.ForeignKey(CGI,)
    # passfail = models.BooleanField(default=False)
    progress = models.CharField(max_length=100, verbose_name="Progress", choices=CHOICES, default="-",
                                help_text="- : Not Yet Tested, 0 : Zero Streak, 1 : One Streak, 2 : Two Streak, M : Mastered",
                                 )
    #comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        if self.progress == "M":
            return '{} has passed CGI {}'.format(self.student.first_name, self.cgi.cgi_number)
        else:
            return '{} is working on CGI {}'.format(self.student.first_name, self.cgi.cgi_number)

    class Meta:
        verbose_name = "CGI Result"
        verbose_name_plural = "CGI Results"
        ordering = ['cgi']