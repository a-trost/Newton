from django.shortcuts import render
import datetime

from brain.models import StudentRoster, Classroom, CurrentClass, AccountInfo, MorningMessage, MorningMessageSettings, \
    Schedule, SubjectUnit, BehaviorReport, SchoolDay
from ixl.models import IXLSkillScores, ChallengeAssignment, ChallengeExercise, IXLSkill
from brain.templatetags import brain_extras
from variables import *
from libs.functions import get_current_amc_challenge, get_current_ixl_challenge, get_nearest_monday


def get_behavior_date_list():  # Last week's behavior
    today = datetime.date.today() # Get today's date
    monday = get_nearest_monday((today - datetime.timedelta(days=4)))
    BEHAVIOR_DATE_LIST = []
    for i in range(5):
        school_day, created = SchoolDay.objects.get_or_create(day=(monday+datetime.timedelta(days=i)))
        BEHAVIOR_DATE_LIST.append(school_day)

    # Make list of monday - Friday school_day objects
    #BEHAVIOR_DATE_LIST = [school_day, school_day, school_day, school_day, school_day,]
        # This list won't be edited once it's created. It'll be used for each student in the loop
    return BEHAVIOR_DATE_LIST


def parent_letters(request, arg):
    # url: /brain/16-17
    if StudentRoster.objects.filter(current_class__grade=arg).exists():
        student_list = StudentRoster.objects.filter(current_class__grade=arg)
    elif StudentRoster.objects.filter(current_class__teacher__last_name=arg).exists():
        student_list = StudentRoster.objects.filter(current_class__teacher__last_name=arg)

    student_list, unit_descriptions, BEHAVIOR_DATE_LIST, mondays_date, export_list = make_parent_letters(student_list)

    return render(request, 'parentletter/parent_letter_print.html',
                  {'student_list': student_list, 'export_list': export_list, 'mondays_date': mondays_date,
                   'BEHAVIOR_DATE_LIST': BEHAVIOR_DATE_LIST, })


def make_parent_letters(student_list):
    mondays_date = get_nearest_monday()
    unit_descriptions = SubjectUnit.objects.filter(
        datestarted__range=(mondays_date - datetime.timedelta(days=2), mondays_date + datetime.timedelta(days=2)))
    BEHAVIOR_DATE_LIST = get_behavior_date_list()
    export_list = get_student_info(student_list, BEHAVIOR_DATE_LIST)

    return student_list, unit_descriptions, BEHAVIOR_DATE_LIST, mondays_date, export_list


def get_student_info(student_list, BEHAVIOR_DATE_LIST):
    export_list = []
    for student in student_list:
        behavior_list = []
        for school_day in BEHAVIOR_DATE_LIST:
            if school_day.noschool == True:
                behavior_list.append("NO SCHOOL")
            else:
                try:
                    behavior_obj = BehaviorReport.objects.get(student=student, school_day=school_day)
                    if behavior_obj.data == "1":
                        behavior_list.append("I Can Do Better")
                    elif behavior_obj.data == "2":
                        behavior_list.append("Okay Self")
                    elif behavior_obj.data == "3":
                        behavior_list.append("Good Self")
                    elif behavior_obj.data == "4":
                        behavior_list.append("Best Self!")
                    else:
                        behavior_list.append("")
                        # TODO: Some kind of catch for if data is weird or if it's missing entirely.
                except:
                    behavior_list.append("")

        # Get current IXL
        try:
            challenge_exercise_list, bonus_exercise_list = get_current_ixl_challenge(student)
        except:
            challenge_exercise_list = None
            bonus_exercise_list = None
        # Get current AMC
        try:
            amc_combinations, amc_test_type, amc_test_name = get_current_amc_challenge(student)
        except:
            amc_combinations, amc_test_type, amc_test_name = None, None, None
        # Check if the AMC is ADD/SUB, otherwise, explain the exercise
        # Add to list
        export_list.append(
            [student, challenge_exercise_list, bonus_exercise_list, amc_combinations, amc_test_type, amc_test_name])
    return export_list




# TODO:  Make script to get last week's homework status
# TODO: This Week Feature - If applicable, the script pulls in paragraphs of current units to discuss what's going on this week