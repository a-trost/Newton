from django.core.management import BaseCommand
from brain.models import Classroom, StudentRoster, CurrentClass, ReadingStats, BehaviorReport, WeeklyWord, \
    SubjectUnit
import datetime
from libs.functions import get_nearest_monday

# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import sys,os
from os import listdir
import re
from brain.models import DataUpdate
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Emails parents to give details about their scholar."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        classroom_info_dict = {} # {"Trost":{"name":"Mr. Trost", "phone":"555-555-5555", "remind_url":"atrosts",
                                # "email":"MrTrost@gmail.com",}, "Teacher2":{...
        classroom_objects = Classroom.objects.filter(currentclass__grade="2nd")
        for classroom in classroom_objects:
            classroom_info_dict[classroom.last_name] = {"name":classroom.title + classroom.last_name, "phone":classroom.workphone,
                                                    "remind_url":classroom.remindURL, "email":classroom.email}

        student_list = StudentRoster.objects.filter(email=None).only("student_id", "first_name", "last_name", "email",
                                                                     "email2")

        mondays_date = get_nearest_monday()
        unit_descriptions = SubjectUnit.objects.filter(datestarted__range=(mondays_date-datetime.timedelta(days=2), mondays_date + datetime.timedelta(days=2)))
        # TODO: RULER Words

        # TODO: Feeling Words
        # TODO: Get IXL Challenge
        # TODO: Get AMC Challenge
        # TODO: Get behavior Report from last week
        # TODO: Get Homework from last week
        # TODO: Format Email
        # title="BTWA: {student}'s Weekly Classroom Report - {date}".format(student,date)
        # TODO: Send Email
        # TODO: When Finished, email classroom with # of parents successfully emailed.
        pass
