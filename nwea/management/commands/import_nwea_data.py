# populate_rit_bands.py

nwea_score_csv = "nwea/management/commands/nweadata.csv"

from django.core.management.base import BaseCommand, CommandError

from nwea.models import NWEAScore, NWEASkill, RITBand, NWEAGoal, NWEAAverage

from brain.models import StudentRoster

import csv

scoreReader = csv.reader(open(nwea_score_csv), delimiter=',', quotechar='"')


class Command(BaseCommand):
    help = 'Creates database entries for all permutations of (NWEADomain, NWEASubDomain, NWEARITBand)'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    # For each of the 8 subdomains that are created already,
    # Make the 14 RIT band options available and save them


    def handle(self, *args, **options):

        for row in scoreReader:
            if row[0] != 'Last Name':  # Ignore the header row, import everything else
                student = StudentRoster.objects.get(last_name=row[0], first_name=row[1])
                reading_fall = row[6]
                math_fall = row[8]
                reading_expected_growth = round(float(row[16]))
                reading_goal = round(float(row[18]))
                math_expected_growth = round(float(row[20]))
                math_goal = round(float(row[22]))
                print("Student: {}, Reading Fall: {}, Math Fall {}, Expected Reading Growth {}".format(student,
                                                                                                       reading_fall,
                                                                                                       math_fall,
                                                                                                       reading_expected_growth,
                                                                                                       ))
                math_winter = float(math_fall) + round(float(math_expected_growth) / 2)
                reading_winter = float(reading_fall) + round(float(reading_expected_growth) / 2)
                obj, created = NWEAGoal.objects.get_or_create(
                    student=student,
                    math_winter=math_winter,
                    math_spring=math_goal,
                    reading_winter=reading_winter,
                    reading_spring=reading_goal,

                )
                obj, created = NWEAAverage.objects.get_or_create(
                    student=student,
                    math_fall=math_fall,
                    reading_fall=reading_fall,

                )
