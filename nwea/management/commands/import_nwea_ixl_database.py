# populate_rit_bands.py

nwea_score_csv="nwea/management/commands/nweadatabase.csv"


from django.core.management.base import BaseCommand, CommandError

from nwea.models import NWEAScore, NWEASkill, RITBand


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
            if row[0] != 'Domain':  # Ignore the header row, import everything else
                domain = row[0]
                subdomain = row[1]
                ritband = row[2]
                skilldescription = row[3]
                ixl_match = row[4]
                rit_band = RITBand.objects.get(domain= domain, subdomain=subdomain, rit_band=ritband)

                obj, created = NWEASkill.objects.get_or_create(
                    rit_band=rit_band,
                    skill = skilldescription,
                    ixl_match = ixl_match
                )

