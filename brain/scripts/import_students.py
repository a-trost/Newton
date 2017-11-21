# scripts/import_students.py

# Full path and name to your csv file
# csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"
csv_filepathname="./grade2students2016.csv"


# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import datetime
import sys,os
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()
from brain.models import StudentRoster, Classroom, CurrentClass


import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

# Start execution
def run():
    for row in dataReader:
        if row[0] != 'Last Name': # Ignore the header row, import everything else
            last_name = row[0]
            first_name = row[1]
            date_of_birth = datetime.datetime.strptime(row[2], "%m/%d/%y").strftime('%Y-%m-%d')
            gender = row[3]
            current_class = CurrentClass.objects.all().get(teacher__last_name=row[4])
            obj, created = StudentRoster.objects.get_or_create(
                last_name= last_name,
                first_name = first_name,
                date_of_birth = date_of_birth,
                gender = gender,
                current_class=current_class,
            )

#run()