import datetime
import random

from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from . import forms
from brain.models import StudentRoster, CurrentClass
from brain.templatetags import brain_extras
from amc.models import AMCTestResult, AMCTest
from variables import *

def school_roster(request,):
    # url: /brain/16-17
    student_list = StudentRoster.objects.all()
          # .order_by('current_class__grade')
                    #.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    teacher_list = CurrentClass.objects.all()
    return render(request, 'amc/index.html',
                  {'student_list': student_list,'teacher_list': teacher_list,})


def grade_list(request, grade="2nd"):  # List of the full student roster
    # url: /brain/16-17/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'grade': grade,})


def class_list(request, grade="2nd", classroom="Trost"):
    # url: /brain/16-17/2nd/trost
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__teacher__last_name=classroom)
    amc_tests = AMCTestResult.objects.all()

    return render(request, 'amc/class_list.html', {'student_list': student_list,'grade': grade,
                                                   'classroom': classroom, 'amc_tests': amc_tests})

# This one is for the Challenge Sheets - Flash Cards
def get_student_and_test_list_for_challenges(student_list):
    student_and_test_list = []
    for student in student_list:
        if student.first_name == "Stephen":
             continue
        elif brain_extras.amc_badges_earned(student) ==10:
            continue
        current_test_number = brain_extras.current_amc_test(
            student)  # Run script to figure out the current test for student
        current_test = AMCTest.objects.get(test_number=current_test_number)  # Get the current test
        current_test_name = current_test.name # Statue of Liberty
        current_test_signifier = current_test.topic # Keeps a string for "Addition 1" or "Subtraction 5" or "Fractions"
        current_test_topic = current_test.topic.replace(" ",
                                                        "").upper()  # Get the Topic (Addition 3) and turn it into ADDITION3
        if 'SUBTRACTION' in current_test_topic:  # This is for the Template so it knows if we're adding or subtracting
            test_type = 'SUB'
        elif "ADDITION" in current_test_topic:
            test_type = 'ADD'
        else:
            test_type = "IMAGE"  # This will be used for clocks, coins, etc.

        first_name = student.first_name  # Split these for ease of use down the line
        last_name = student.last_name
        # Now put all the information into the tuple and append the tuple to the list
        combinationset = TESTDICTIONARY[current_test_topic]
        # finallist order will go [(1,2), (1,3), (1,4)..., (1,9), 3, 4, 5... 10], [(2,2)...4]
        tempcombolist = []
        tempanswerlist = []
        finallist = []
        for combination in combinationset:
            # Get the first combination and add it to a short combo list
            var1, var2 = combination
            tempcombolist.append((var1, var2))
            # Add those two numbers together and add that to a short answer list
            if test_type == 'ADD':
                tempanswerlist.append(var1+var2)
            elif test_type == 'SUB':
                tempanswerlist.append(var1 - var2)
            elif test_type == 'IMAGE':
                tempanswerlist.append(var2)
            # Repeat until you have 10 items in both lists, then append those lists together into one list.
            if len(tempcombolist) == 10:
            # Then put that list as a new item at the end of the big list.
                tempanswerlist[0], tempanswerlist[1] = tempanswerlist[1], tempanswerlist[0]
                tempanswerlist[2], tempanswerlist[3] = tempanswerlist[3], tempanswerlist[2]
                tempanswerlist[4], tempanswerlist[5] = tempanswerlist[5], tempanswerlist[4]
                tempanswerlist[6], tempanswerlist[7] = tempanswerlist[7], tempanswerlist[6]
                tempanswerlist[8], tempanswerlist[9] = tempanswerlist[9], tempanswerlist[8]
                j = tempcombolist + tempanswerlist
                finallist.append(j)
                tempcombolist = []
                tempanswerlist = []
        if len(tempcombolist):
            while len(tempcombolist) != 10:
                tempcombolist.append('None')
                tempanswerlist.append('None')
            tempanswerlist[0], tempanswerlist[1] = tempanswerlist[1], tempanswerlist[0]
            tempanswerlist[2], tempanswerlist[3] = tempanswerlist[3], tempanswerlist[2]
            tempanswerlist[4], tempanswerlist[5] = tempanswerlist[5], tempanswerlist[4]
            tempanswerlist[6], tempanswerlist[7] = tempanswerlist[7], tempanswerlist[6]
            tempanswerlist[8], tempanswerlist[9] = tempanswerlist[9], tempanswerlist[8]
            j = tempcombolist + tempanswerlist
            finallist.append(j)
            tempcombolist = []
            tempanswerlist = []

        student_list_entry = (first_name, last_name, current_test_name, test_type,
                              finallist, current_test_signifier)

        student_and_test_list.append(student_list_entry)
    return student_and_test_list

# This one is for the Test Sheets
def get_student_and_test_list_for_tests(student_list):
    student_and_test_list = []
    for student in student_list:
        if student.first_name == "Stephen":
            continue
        elif brain_extras.amc_badges_earned(student) ==10:
            continue
        current_test_number = brain_extras.current_amc_test(
            student)  # Run script to figure out the current test for student
        current_test = AMCTest.objects.get(test_number=current_test_number)  # Get the current test
        current_test_name = current_test.name
        current_test_signifier = current_test.topic # Keeps a string for "Addition 1" or "Subtraction 5" or "Fractions"
        current_test_topic = current_test.topic.replace(" ",
                                                        "").upper()  # Get the Topic (Addition 3) and turn it into ADDITION3
        if 'SUBTRACTION' in current_test_topic:  # This is for the Template so it knows if we're adding or subtracting
            test_type = 'SUB'
        elif "ADDITION" in current_test_topic:
            test_type = 'ADD'
        else:
            test_type = "IMAGE"  # This will be used for clocks, coins, etc.

        first_name = student.first_name  # Split these for ease of use down the line
        last_name = student.last_name
        # Randomize Combinations and pull first 20 from list. If you run out of combos, loop around.
        problem_list = TESTDICTIONARY[current_test_topic]
        random.shuffle(problem_list)
        test_list = []
        for i in problem_list:
            test_list.append(i)
        if test_type == 'IMAGE':
            test_list = test_list[:9]
        else:
            test_list=test_list[:20]
            if len(test_list) < 20:
                n = 0
                while len(test_list) < 20:
                    test_list.append(test_list[n])
                    n += 1
        # Now put all the information into the tuple and append the tuple to the list
        student_list_entry = (first_name, last_name, current_test_name, test_type,
                              test_list, current_test_signifier)
        student_and_test_list.append(student_list_entry)
    return student_and_test_list

# This one is for the Test Sheets
def spring_cba_test(student_list, test_type):
    student_and_test_list = []
    for student in student_list:
        if test_type == "ADD":
            test_type = 'ADD'
            current_test_name = "CBA Addition Facts"

            problem_list = SPRINGADDITION
        elif test_type == 'SUB':
            current_test_name = "CBA Subtraction Facts"

            test_type = 'SUB'
            problem_list = SPRINGSUBTRACTION
        first_name = student.first_name  # Split these for ease of use down the line
        last_name = student.last_name
        # Randomize Combinations and pull first 20 from list. If you run out of combos, loop around.
        random.shuffle(problem_list)
        test_list = []
        for i in problem_list:
            test_list.append(i)
        test_list=test_list[:20]
        if len(test_list) < 20:
            n = 0
            while len(test_list) < 20:
                test_list.append(test_list[n])
                n += 1
        # Now put all the information into the tuple and append the tuple to the list
        student_list_entry = (first_name, last_name, current_test_name, test_type,
                              test_list)
        student_and_test_list.append(student_list_entry)
    return student_and_test_list


def print_challenge_sheets_class(request,  grade="2nd", classroom="Trost"):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__teacher__last_name=classroom)
    student_and_test_list = get_student_and_test_list_for_challenges(student_list)

    return render(request, 'amc/amc_card_print.html',
                  {'grade': grade, 'classroom': classroom, 'student_and_test_list': student_and_test_list})


def print_challenge_sheets_grade(request, grade="2nd"):
    student_list = StudentRoster.objects.filter(current_class__grade=grade)
    student_and_test_list = get_student_and_test_list_for_challenges(student_list)
    return render(request, 'amc/amc_card_print.html',
                  { 'grade': grade, 'student_and_test_list': student_and_test_list,})


def print_test_sheets_class(request,  grade="2nd", classroom="Trost"):

    # Get list of students in this class
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__teacher__last_name=classroom)
    # Use list of students and the current test they're taking.
    student_and_test_list=get_student_and_test_list_for_tests(student_list)
    random_list = [0,1,2,3]



    return render(request, 'amc/amc_test_print.html',
                  {'grade': grade, 'classroom': classroom, 'student_and_test_list': student_and_test_list, 'random_list':random_list,})


def print_test_sheets_grade(request, grade="2nd", classroom="Trost"):
    # Get list of students in this grade
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
    # Use list of students and the current test they're taking.
    student_and_test_list=get_student_and_test_list_for_tests(student_list)
    random_list = [0,1,2,3]
    return render(request, 'amc/amc_test_print.html',
                  {'grade': grade, 'classroom': classroom, 'student_and_test_list': student_and_test_list,
                   'random_list':random_list})


################    CBA    ##############################

def print_cba_test_sheets_class(request,  grade="2nd", classroom="Trost", test_type='addition'):
    # Get list of students in this class
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__teacher__last_name=classroom)
    # Use list of students and the current test they're taking.
    student_and_test_list=get_student_and_test_list_for_tests(student_list)
    if test_type == 'add':
        test_type = "ADD"
    elif test_type == 'sub':
        test_type = "SUB"
    student_and_test_list =spring_cba_test(student_list, test_type)
    random_list = [0,1,2,3]

    return render(request, 'amc/cba_test_print.html',
                  {'grade': grade, 'classroom': classroom, 'student_and_test_list': student_and_test_list,
                   'random_list':random_list,})


def print_cba_test_sheets_grade(request,  grade="2nd", classroom="Trost", type='addition'):
    # Get list of students in this grade
    student_list = StudentRoster.objects.filter(current_class__grade=grade)
    # Use list of students and the current test they're taking.
    if type == 'addition':
        test_type = "ADD"
    elif type == 'subtraction':
        test_type = "SUB"
    student_and_test_list =spring_cba_test(student_list, test_type)
    random_list = [0,1,2,3]

    return render(request, 'amc/cba_test_print.html',
                  { 'grade': grade, 'classroom': classroom, 'student_and_test_list': student_and_test_list,
                   'random_list':random_list})



@login_required
def input_amc_scores(request,  grade="2nd", classroom="Trost"):
    if request.method == 'POST':
        TestListFormSet = formset_factory(forms.InputAMCScores, extra=0)
        formset = TestListFormSet(request.POST)
        has_errors = False
        for form in formset:
            # Seems like it should be possible to have the form know the instance it was created from, and update
            # that rather than go through this manual process
            if form.is_valid():
                form.save()
            else:
                existing_results = AMCTestResult.objects.filter(student=form.instance.student,
                                                                date_tested=form.instance.date_tested)
                if form.instance.score and existing_results.count():
                    instance = existing_results.first()
                    instance.score = form.instance.score
                    instance.save()
                else:
                    has_errors = True
                    print(form.errors)
        messages.add_message(request, messages.SUCCESS, "American Math Challenges Recorded!")
        if not has_errors:
            url = reverse('amc:classlist', kwargs={'grade': grade, 'classroom': classroom})
            return HttpResponseRedirect(url)
    else:
        student_list = StudentRoster.objects.filter(current_class__grade=grade) \
            .filter(current_class__teacher__last_name=classroom)

        form_count = student_list.count()
        TestListFormSet = formset_factory(forms.InputAMCScores, extra=form_count)
        formset = TestListFormSet()
        # Would be nice to create forms from the instances rather than manually set initial, but that did not seem
        # to work correctly
        for i in range(form_count):
            today = datetime.date.today()
            existing_results = AMCTestResult.objects.filter(student=student_list[i], date_tested=today)
            initial_test = brain_extras.current_amc_test(student_list[i])
            if existing_results.count():
                instance = existing_results.first()
                formset.forms[i].instance = instance
                initial_student = instance.student
                initial_score = instance.score
            else:
                initial_student = student_list[i]
                initial_score = None
            formset.forms[i].fields['student'].initial = initial_student
            formset.forms[i].fields['test'].initial = initial_test
            formset.forms[i].fields['score'].initial = initial_score


    return render(request, 'amc/input_amc_scores_form.html', {
        'formset': formset,
        'classroom': classroom,
        'grade': grade,

    })

