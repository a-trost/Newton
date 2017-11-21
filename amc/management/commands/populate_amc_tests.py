# scripts/populate_amc_tests.py

# Full path and name to your csv file
# csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"
csv_filepathname="amc/management/commands/amctests.csv"


# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import sys,os
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()
from amc.models import AMCTest

from django.core.management.base import BaseCommand, CommandError

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

class Command(BaseCommand):
    help = 'Updates the student Roster by importing a CSV'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    def handle(self, *args, **options):
        for row in dataReader:
            if row[0] != 'Last Name':  # Ignore the header row, import everything else
                test_number = row[0]
                topic = row[1]
                name = row[2]
                grade_equivalent = row[3]
                total_questions = row[4]
                minimum_passing_grade = row[5]


                obj, created = AMCTest.objects.get_or_create(
                    test_number=test_number,
                    topic=topic,
                    name=name,
                    grade_equivalent=grade_equivalent,
                    total_questions=total_questions,
                    minimum_passing_grade=minimum_passing_grade,
                )




