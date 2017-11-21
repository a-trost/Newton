# commands/createchallenges.py

# Full path to your django project directory
your_djangoproject_home = "/home/alex/newton/"
import django
import datetime
import sys, os

from variables import second_classrooms as assigned_teachers
from variables import mastery_skills, cbaExercises, mailgun_apikey
from libs.functions import get_nearest_monday, get_student_list, create_ixl_challenge

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()

from django.core.management.base import BaseCommand, CommandError
#
# from brain.models import StudentRoster, CurrentClass, Classroom
# from ixl.models import ChallengeAssignment, Challenge, ChallengeExercise, IXLSkillScores
# from libs.functions import make_mastery_challenge, make_cba_challenge, make_nwea_challenge

class Command(BaseCommand):
    help = 'Assigns a custom challenge to all students'

    def add_arguments(self, parser):
            pass

    #### START RUN FUNCTION
    def handle(self, *args, **options):

        student_list = get_student_list(grade="2nd")
        self.stdout.write("Got student list. Creating Challenges.")
        for student in student_list:  # Go through one student at a time
            obj, created = create_ixl_challenge(student)
        # TODO: Email teachers previous week's scores
        # TODO: Add Bonus Exercises
        # IXL Challenge Creation
        # Create 5 main challenges
        # 2 for CBA
        # Map the CBAs to IXL Exercises for each of the three.
        # Make it change depending on the date
        # 2 for NWEA
        # 1 for Mastery - based on the current or passed curriculum - 100 Smart Score
        # Create 5 Bonus Challenges
