your_djangoproject_home="/home/alex/newton/"
import django
from datetime import date
import sys,os
from os import listdir
import re

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()
import random
from django.core.management.base import BaseCommand, CommandError

from brain.models import StudentRoster, ReadingStats, CurrentClass, ReadingTimeSpent, StreakHighScore
from ixl.models import IXLSkillScores, IXLStats, ChallengeAssignment, IXLTimeSpent
from badges.models import StickerAssignment, Sticker

# BOOKS_READ = [(50, 'read-50-books'), (100, 'read-100-books'), (200, 'read-200-books'), (300, 'read-300-books'),
#               (400, 'read-400-books'), (500, 'read-500-books'), (600, 'read-600-books'),]
#
# MYON_TIME = [(200, 'read-200-minutes'), (400, 'read-400-minutes'), (600, 'read-600-minutes'),
#              (800, 'read-800-minutes'), (1000, 'read-1000-minutes'), (2000, 'read-2000-minutes'),
#              (3000, 'read-3000-minutes'), (4000, 'read-4000-minutes'), (5000, 'read-5000-minutes'),
#              ]

MYON_GROWTH = [
     (25, 'grow-25-lexile'), (50, 'grow-50-lexile'),
    (75, 'grow-75-lexile'), (100, 'grow-100-lexile'), (150, 'grow-150-lexile'), (200, 'grow-200-lexile'),
    (250, 'grow-250-lexile'), (300, 'grow-300-lexile'), (350, 'grow-350-lexile'), (400, 'grow-400-lexile'),
    ]


SATURDAY_SCHOLAR = [
    (1, 'saturday-scholar-1'), (5, 'saturday-scholar-5'), (10, 'saturday-scholar-10'), (20, 'saturday-scholar-20'),
    (30, 'saturday-scholar-30'),
]

SUNDAY_SCHOLAR = [
    (1, 'sunday-scholar-1'), (5, 'sunday-scholar-5'), (10, 'sunday-scholar-10'), (20, 'sunday-scholar-20'),
    (30, 'sunday-scholar-30'),
]

LEXILE_LEVEL = [
    (100, 'lexile-100'), (200, 'lexile-200'), (300, 'lexile-300'), (400, 'lexile-400'), (500, 'lexile-500'),
    (600, 'lexile-600'), (700, 'lexile-700'), (800, 'lexile-800'),(900, 'lexile-900'),(1000, 'lexile-1000'),(1100, 'lexile-1100'),
    ]

IXL_CHALLENGES = [
    (1, '1-ixl-challenges'), (2, '2-ixl-challenges'), (3, '3-ixl-challenges'), (4, '4-ixl-challenges'),
    (5, '5-ixl-challenges'), (10, '10-ixl-challenges'), (15, '15-ixl-challenges'), (20, '20-ixl-challenges'),
    (25, '25-ixl-challenges'), (30, '30-ixl-challenges'),
    ]

IXL_TIME = [(200, 'ixl-200-minutes'), (400, 'ixl-400-minutes'), (600, 'ixl-600-minutes'), (800, 'ixl-800-minutes'),
            (1000, 'ixl-1000-minutes'), (1200, 'ixl-1200-minutes'), (1400, 'ixl-1400-minutes'),
            (1600, 'ixl-1600-minutes'), (1800, 'ixl-1800-minutes'), (2000, 'ixl-2000-minutes'),
            ]

MYON_STARS = [
    (10, '10-myon-stars'),  (20, '20-myon-stars'),
     (30, '30-myon-stars'),(40, '40-myon-stars'),(50, '50-myon-stars'),
   (75, '70-myon-stars'), (100, '100-myon-stars'),
    (150, '150-myon-stars'),(200, '200-myon-stars'),
]

IXL_STARS = [
     (10, '10-ixl-stars'), (20, '20-ixl-stars'),
    (30, '30-ixl-stars'), (40, '40-ixl-stars'), (50, '50-ixl-stars'),
  (75, '70-ixl-stars'), (100, '100-ixl-stars'),
    (150, '150-ixl-stars'),  (200, '200-ixl-stars'),
]

IXL_STREAK = [ (7, 'ixl-streak-7'), (10, 'ixl-streak-10'), (15, 'ixl-streak-15'), (20, 'ixl-streak-20'), (25, 'ixl-streak-25'),
(30, 'ixl-streak-30'), (40, 'ixl-streak-40'), (50, 'ixl-streak-50'), (60, 'ixl-streak-60'), (70, 'ixl-streak-70'),
]

MYON_STREAK = [ (7, 'myon-streak-7'), (10, 'myon-streak-10'), (15, 'myon-streak-15'), (20, 'myon-streak-20'), (25, 'myon-streak-25'),
(30, 'myon-streak-30'), (40, 'myon-streak-40'), (50, 'myon-streak-50'), (60, 'myon-streak-60'), (70, 'myon-streak-70'),
]

class Command(BaseCommand):
    help = 'Makes sticker objects for achievements'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    def handle(self, *args, **options):
        checkbadges("2nd")



def checkbadges(grade):
    # Get student_list
    student_list = StudentRoster.objects.filter(classroom__grade__icontains=grade)
    for student in student_list:
        print("{} {}".format(student.first_name, student.last_name))
        reading_stats = ReadingStats.objects.filter(student=student).first()
        ixl_stats = IXLStats.objects.get(student=student)
        ixl_time_spent = IXLTimeSpent.objects.filter(student=student)
        ixl_stars = 0
        for log in ixl_time_spent:
            if log.time_goal_met():
                ixl_stars +=1
        myon_time_spent = ReadingTimeSpent.objects.filter(student=student).filter(time_spent__gte=600)
        myon_stars = myon_time_spent.count()
        saturday_set = set()
        sunday_set = set()
        for log in ixl_time_spent:
            if log.date_spent.weekday() == 5:
                if log.time_goal_met():
                    saturday_set.add(log.date_spent)
            elif log.date_spent.weekday() == 6:
                if log.time_goal_met():
                    sunday_set.add(log.date_spent)
        for log in myon_time_spent:
            if log.date_spent.weekday() == 5:
                if log.time_goal_met():
                    saturday_set.add(log.date_spent)
            elif log.date_spent.weekday() == 6:
                if log.time_goal_met():
                    sunday_set.add(log.date_spent)

        ixl_streak = StreakHighScore.objects.filter(student=student).filter(site="IXL").first()
        myon_streak = StreakHighScore.objects.filter(student=student).filter(site="MYON").first()


        completed_challenges = 0
        ixl_challenges = ChallengeAssignment.objects.filter(student_id=student)

        for challenge in ixl_challenges:
            total_complete, total_questions = challenge.completed()
            #print("Challenge {} is {}".format(challenge,complete))
            if total_complete == total_questions:
                completed_challenges += 1
                #print("Completed Challenges = {}".format(completed_challenges))

        for benchmark in MYON_GROWTH:
            if reading_stats.lexile_progress >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in MYON_STREAK:
            if myon_streak.days_in_a_row >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in IXL_STREAK:
            if ixl_streak.days_in_a_row >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in MYON_STARS:
            if myon_stars >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in IXL_STARS:
            if ixl_stars >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in LEXILE_LEVEL:
            if reading_stats.current_lexile >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in IXL_CHALLENGES:
            if completed_challenges >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in SATURDAY_SCHOLAR:
            if len(saturday_set) >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in SUNDAY_SCHOLAR:
            if len(sunday_set) >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break
        # if len(cgiresults)==13:
        #     all_finished = True
        #     for result in cgiresults:
        #         if result.progress == '3' or result.progress =='M':
        #             pass
        #         else:
        #             all_finished = False
        #     if all_finished:
        #         sticker = Sticker.objects.get(slug='cgi-all-passed')
        #         obj,created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
        #
        #     for result in cgiresults:
        #         if result.progress == '3' or result.progress =='M':
        #             sticker = Sticker.objects.get(slug='cgi-{}-passed'.format(result.cgi.cgi_number))
        #             obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)




       # for benchmark in MYON_TIME:
        #     if reading_stats.myon_time_spent >= benchmark[0]:
        #         sticker = Sticker.objects.get(slug=benchmark[1])
        #         obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
        #     else:
        #         break
        #
        # for benchmark in BOOKS_READ:
        #     if reading_stats.myon_books_finished >= benchmark[0]:
        #         sticker = Sticker.objects.get(slug=benchmark[1])
        #         obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
        #     else:
        #         break