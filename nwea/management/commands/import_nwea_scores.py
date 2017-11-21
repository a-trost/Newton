# populate_rit_bands.py

nwea_score_csv="nwea/management/commands/nweascores.csv"


from django.core.management.base import BaseCommand, CommandError

from nwea.models import NWEAScore, NWEASkill, RITBand

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
            if row[0] != 'Last':  # Ignore the header row, import everything else
                student = StudentRoster.objects.get(last_name=row[0], first_name=row[1])
                subdomain1 = row[2]
                subdomain2 = row[3]
                subdomain3 = row[4]
                subdomain4 = row[5]
                subdomain5 = row[6]
                subdomain6 = row[7]
                subdomain7 = row[8]
                subdomain8 = row[9]
                season = row[11]

                obj, created = NWEAScore.objects.get_or_create(
                    student = student,
                    subdomain1 = subdomain1,
                    subdomain2 = subdomain2,
                    subdomain3 = subdomain3,
                    subdomain4 = subdomain4,
                    subdomain5 = subdomain5,
                    subdomain6 = subdomain6,
                    subdomain7 = subdomain7,
                    subdomain8 = subdomain8,
                    season = season,

                )

