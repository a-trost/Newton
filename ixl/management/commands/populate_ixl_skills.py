# populate_ixl_skills.py

from django.core.management.base import BaseCommand, CommandError

from ixl.models import IXLSkillScores, IXLSkill

class Command(BaseCommand):
    help = 'Creates database entries for all IXL skills'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    import csv
    csv_filepathname = "/home/alex/newton/ixl/management/commands/IXLMaster.csv"

    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')


    def handle(self, *args, **options):
        for row in self.dataReader:
            if row[0] != 'Category':  # Ignore the header row, import everything else
                category = row[2]
                skill_id = row[0]
                skill_description = row[1]
                obj, created = IXLSkill.objects.get_or_create(
                    category=category, skill_id=skill_id, skill_description=skill_description,
                )

