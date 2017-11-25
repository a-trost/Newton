# populate_ixl_skills.py

from django.core.management.base import BaseCommand, CommandError

from ixl.models import IXLListSkill

class Command(BaseCommand):
    help = 'Creates database entries for all IXL skills'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    import csv
    csv_filepathname = "/home/alex/newton/ixl/management/commands/IXLMaster-GradesBased.csv"

    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')


    def handle(self, *args, **options):
        for row in self.dataReader:
            if row[0] != 'Category':  # Ignore the header row, import everything else
                category = row[0]
                grade = row[1][0]
                id_code = row[1][2:]
                description = row[2]
                obj, created = IXLListSkill.objects.get_or_create(
                    category=category, id_code=id_code, description=description, grade=grade,
                )
                if created:
                    print("{}-{} was created!".format(grade, id_code))
