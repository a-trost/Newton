# scripts/load_ixl_skills.py

# Full path and name to your csv file
csv_filepathname="./ixl-gradebook-example.csv"

# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import sys,os
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")
django.setup()

import re
import csv
from datetime import datetime

from brain.models import StudentRoster
from ixl.models import IXLSkill, IXLSkillScores
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

def import_ixl_scores(csv_filepathname):
    indexed = False
    if check_exercise_accuracy():
        print("All Exercises match.")
        dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
        for row in dataReader:
            if row[0] == 'Category':# Go through and replace student names with their Newton IDs.
                if not indexed:
                    count = 3
                    for column in row:
                        if column in ['Category','Skill code','Skill name',]:
                            continue
                        elif column not in ['Category','Skill code','Skill name',]:
                            namesRegex = re.compile(r'([a-zA-Z\'-]+)\s([a-zA-Z\'-]+)')
                            mo = namesRegex.search(column)
                            student_id = StudentRoster.objects.get(first_name=mo.group(1), last_name=mo.group(2))
                            row[count] = student_id.student_id
                        count += 1
                    names_list = row
                    print(names_list)
                    indexed = True

            # For the rest of the rows:
            else:
                current_skill_id = row[1]
                count = 0
                for column in row:
                    print("{} is the column. The skill ID is {}".format(column, current_skill_id))
                    if is_number(column):

                        score = int(column)
                        student_id = StudentRoster.objects.get(student_id=names_list[count])
                        skill_id = IXLSkill.objects.get(skill_id=current_skill_id)
                        print("Found a number. The number is {}".format(column))
                        #ixl_skill_id = skill_id.pk
                        date = datetime.today()
                        print("Score: {}  Student: {}  IXL: {} Date: {}".format(score, student_id, skill_id, date))
                        defaults = {'score': score, 'date_recorded': date,}
                        obj, created = IXLSkillScores.objects.update_or_create(
                            student_id = student_id,
                            ixl_skill_id = skill_id,
                            defaults = defaults
                            )
                    else:
                        print("{} is not a number".format(column))
                    count += 1
    else:
        print("Exercises have changed!")
        sys.exit()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def check_exercise_accuracy():
# 1. Check all exercises are the same, if so, go to the rest of the script.
    output = True
    for row in dataReader:
        if row[0] == 'Category':
            pass
        else:
            try:
                skill = IXLSkill.objects.get(category=row[0], skill_id=row[1], skill_description=row[2])
            except IndexError:
                output = False
                print("There was no IXL Skill found with Category {}, ID {}, and Description {}".format(row[0], row[1], row[2]))
                # Raise the alarm.
                # Start fixing what has been changed.
                # fix_changed_skills()
    return output

def fix_changed_skills():
    pass
    # 3. Delete all student scores

    # Find changed Exercises
    # for row in dataReader:
    #     if row[0] == 'Category':
    #         pass
    #     else:
    #         try:
    #             skill = IXLSkill.objects.get(category=row[0], skill_id=row[1], skill_description=row[2])
    #         except IndexError:
    #     # Find what the exercise has changed to.
    #             try:
    #                 # See if the skill exists, but under a different Skill ID
    #                 old_skill = IXLSkill.objects.get(category=row[0], skill_description=row[2])

    # 5. Re-Map NWEA to IXL associations.
    # Make a log of newly added IXL Skills
    # Wipe the old skill list and import this new one.
    # 6. Continue on to the rest of the script.
# First thing in this script.
# Go through every exercise in the CSV and make sure the exercises in our database match.
# If they don't:
# Search the database to find a matching exercise:
    # Same First Letter (D)
    # Same description
    # Same Category
# order in csv: category, skill_id, skill_description



