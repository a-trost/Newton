# scripts/import_students.py

# Full path and name to your csv file
# csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"

# Full path to your django project directory
your_djangoproject_home = "/home/alex/newton/"
import django
import datetime
import sys, os

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()

from django.core.management.base import BaseCommand, CommandError

from brain.models import StudentRoster, CurrentClass, Classroom
from ixl.models import ChallengeAssignment, Challenge, ChallengeExercise, IXLSkillScores
from variables import cbaExercises
from libs.functions import nwea_recommended_skills_list as nwea_skills

assigned_classrooms = ['McPherson', 'Trost', 'Ryan', 'Palermo']

cba_exercises2 = ['D-G.5', 'D-M.6', 'D-W.2', 'D-N.2', 'D-B.6', 'D-H.4',
                 'D-G.6',
                 'D-H.6',
                 'D-L.9',
                 'D-L.8',
                 'D-N.5',
                 'D-N.5',
                 'D-Q.5',
                 'D-P.4',
                 'D-S.2',
                 'D-R.2',
                 'D-R.8',
                 'D-R.12',

                 ]
report_card_exercises = ['D-S.2',
                 'D-T.3',
                 'D-R.2',
                 'D-R.4',
                 'D-Q.5',
                 'D-R.7',
                 'D-R.8',
                 'D-B.2',
                 'D-C.4',
                 'D-W.2',
                 'D-C.5',
                 'D-G.15',
                 'D-I.3',
                 'D-E.23',
                 'D-I.2',
                 'D-Y.5',
                         # Unit 6
                         'D-A.7', 'D-P.10', 'D-P.12', "D-E.22", "D-R.12", "D-R.13", "D-Q.15", "D-R.7", "D-R.8","D-O.1"

                 ]

class Command(BaseCommand):
    help = 'Assigns a custom challenge to everyone in the classes listed.'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    def handle(self, *args, **options):
        for classroom in assigned_classrooms:
            try:  # Get the class
                current_class = CurrentClass.objects.get(classroom__last_name=classroom)
            except:
                print('Classroom {} could not be found.'.format(classroom))
                break
            print("Getting student list")
            student_list = StudentRoster.objects.filter(current_class=current_class)
            print("Got student list. Creating Challenges.")
            for student in student_list:  # Go through one student at a time
                # Create the new Challenge
                # print("Setting the date")
                date = datetime.date.today()
                # print("Set the date. Formatting date with strf time")
                date = date.strftime('%-m/%-d')
                # print("Formatted the date. Setting the title with format")

                title = "{} {}'s {} Report Card Challenge".format(student.first_name, student.last_name[0], date)
                # print("Creating current challenge.")
                todays_date = datetime.date.today()
                current_challenge = Challenge.objects.create(title=title, date=todays_date)

                # skill_list = nwea_skills(student,"recommended_skill_list")
                # classrooms_addition = 'None'
                exercise_count = 0
                for cba_skill in cbaExercises:
                    if exercise_count >= 5:
                        pass
                    else:
                        try:
                            skill_score = IXLSkillScores.objects.get(student_id=student,
                                                                     ixl_skill_id__skill_id=cba_skill)
                            if skill_score.score < 80:
                                exercise_count += 1
                                challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                                      exercise_id=cba_skill)
                        except:
                            exercise_count += 1
                            challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                                  exercise_id=cba_skill)

                # for skill in skill_list:
                #     if skill[3] in domain_list or exercise_count >= 5:
                #         pass
                #     else:
                #         exercise_count += 1
                #         domain_list.append(skill[3]) # Add this domain to the list
                #         # Create a Challenge Exercise object with the challenge and skill
                #         challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge, exercise_id=skill[0])

                print("Assigning {} to {}".format(title, student))

                obj, created = ChallengeAssignment.objects.get_or_create(
                    student_id=student, challenge=current_challenge,
                )
                # Get the student list of that class
                # Iterate through the class list
                # Create the relationship between each kid in the class and the designated challenge
