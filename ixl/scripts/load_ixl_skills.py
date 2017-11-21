# scripts/load_ixl_skills.py

# Full path and name to your csv file
csv_filepathname="./IXLMaster.csv"

# Full path to your django project directory
your_djangoproject_home="/Users/alexandertrost/PycharmProjects/newton/"
import django
import sys,os
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")
django.setup()
from ixl.models import IXLSkill


import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

# Start execution
def run():
    for row in dataReader:
        if row[0] != 'Category': # Ignore the header row, import everything else
            category = row[0]
            skill_id = row[1]
            skill_description = row[2]
            obj, created = IXLSkill.objects.get_or_create(
                category=category, skill_id=skill_id, skill_description=skill_description,
            )

def delete_then_run():
    IXLSkill.objects.all().delete()
    run()

