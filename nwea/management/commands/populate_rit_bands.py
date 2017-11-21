# populate_rit_bands.py

from django.core.management.base import BaseCommand, CommandError

from nwea.models import NWEAScore, NWEASkill, RITBand

class Command(BaseCommand):
    help = 'Creates database entries for all permutations of (NWEADomain, NWEASubDomain, NWEARITBand)'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass


# For each of the 8 subdomains that are created already,
    # Make the 14 RIT band options available and save them


    def handle(self, *args, **options):

        SUBDOMAINS = [(1, 1), (1, 2), (2, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8)]
        RIT_CHOICES = (
            (111, '111'),
            (121, '121'),
            (131, '131'),
            (141, '141'),
            (151, '151'),
            (161, '161'),
            (171, '171'),
            (181, '181'),
            (191, '191'),
            (201, '201'),
            (211, '211'),
            (221, '221'),
            (231, '231'),
            (241, '241'),
        )

        for item in SUBDOMAINS:
            current_domain = item[0]
            current_sub = item[1]
            for rit_choice, _ in RIT_CHOICES:
                new_rit_band, created= RITBand.objects.get_or_create(subdomain=current_sub, domain=current_domain, rit_band=rit_choice)
                #print("The new rit band is: %s" % new_rit_band)
                #new_rit_band.save()




