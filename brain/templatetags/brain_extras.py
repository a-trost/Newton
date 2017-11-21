from django import template, forms
import datetime
from brain.models import StudentRoster, CurrentClass, Classroom, Schedule
from amc.models import AMCTestResult, AMCTest, AMCStartingTest
from ixl.models import IXLSkill, IXLSkillScores, ChallengeAssignment
from nwea.models import NWEASkill, NWEAScore, RITBand
from django.utils.timezone import now
from libs.functions import nwea_recommended_skills_list as nwea_skills
from scoreit.models import Score, TeacherApproval

register = template.Library()

#=========================================================================================================
#                                           GENERAL
#=========================================================================================================
@register.filter(name='boys_and_girls')
def gender(value):
    boys, girls = 0,0
    for student in value:
        if student.gender == "M":
            boys +=1
        elif student.gender == "F":
            girls +=1

    boys_and_girls = "{} Boys and {} Girls".format(boys, girls)
    return boys_and_girls


@register.filter
def index(List, i):
    return List[int(i)]

#=========================================================================================================
#                                           AMC
#=========================================================================================================
@register.filter(name='current_amc_test')
def current_amc_test(student):
    """Gets the current AMC test for a student"""
    if AMCTestResult.objects.all().filter(student_id=student):
        last_test_taken = AMCTestResult.objects.all().filter(student_id=student).order_by('-date_tested')[0]
        if last_test_taken.passing_score():
            amc_test = last_test_taken.test.test_number + 1
        elif not last_test_taken.passing_score():
            amc_test = last_test_taken.test.test_number
        else:
            amc_test = "Error"

        return amc_test
    else:
        if AMCStartingTest.objects.all().filter(student_id=student):
            start = AMCStartingTest.objects.get(student_id=student).starting_test
            return start
        else:
            return 1


@register.filter(name='amc_number_to_text')
def amc_number_to_text(value):
    return AMCTest.objects.filter(test_number=value).first()


@register.filter(name='amc_number_of_test_attempts')
def amc_number_of_test_attempts(value, test):
    student = value
    if AMCTestResult.objects.all().filter(student_id=student).filter(test=test):
        count = AMCTestResult.objects.all().filter(student_id=student).filter(test=test).count()
        return count
    else:
        return 0


@register.filter(name='amc_grade_equivalent')
def amc_grade_equivalent(value):
    """Turns a current AMC test number into the grade equivalent."""
    output = AMCTest.objects.filter(test_number=value).first()
    if output:
        output = output.grade_equivalent
    return output


@register.filter(name='amc_badges_earned')
def amc_badges_earned(value):
    test_list = AMCTestResult.objects.all().filter(student=value)
    x = 0
    for test in test_list:
        passed = test.passing_score()
        if passed:
            x += 1
    return x


@register.filter(name='amc_classroom_badges_earned')
def amc_classroom_badges_earned(value):
    x = 0
    for student in value:
        test_list = AMCTestResult.objects.all().filter(student=student)
        for test in test_list:
            passed = test.passing_score()
            if passed:
                x += 1
    return x

@register.filter(name='amc_average_grade_equivalent')
def amc_average_grade_equivalent(value):
    """Turns a current AMC test number into the grade equivalent."""
    if value:
        y = 0 # Total for average
        x = 0 # Counter for average
        for student in value:
            x +=1
            y = y + current_amc_test(student)
        try:
            avg = round(y/x)
        except ZeroDivisionError:
            avg = 1
        try:
            output = AMCTest.objects.filter(test_number=avg).first() # Gets the test that matches that number
            output = output.grade_equivalent
        except:
            output = None
        return output or None
    else:
        return "No Students"

#=========================================================================================================
#                                              IXL
#=========================================================================================================


@register.filter(name='get_ixl_url')
def get_ixl_url(value):
    skill_id = value.upper()
    skill = IXLSkill.objects.all().get(skill_id=skill_id)
    description_string = skill.skill_description.replace('-', '').replace("'", '').replace(",", "").replace('/', '') \
        .replace('?', '').replace('.', '').replace(':', '').replace('$1', 'one dollar').replace("$5", "five dollars")
    description_string = description_string.replace('   ', ' ').replace('  ', ' ')
    description_string = description_string.replace(' ', '-')
    url = str("https://www.ixl.com/math/level-" + skill.skill_id[0] + '/' + description_string).lower()
    return url


@register.filter(name='challenges_completed')
def challenges_completed(student):
    completed_challenges = 0
    ixl_challenges = ChallengeAssignment.objects.filter(student_id=student)
    for challenge in ixl_challenges:
        complete = challenge.completed()
        # print("Challenge {} is {}".format(challenge,complete))
        if complete == "COMPLETE":
            completed_challenges += 1
    return completed_challenges

@register.filter(name='seconds_to_minutes')
def seconds_to_minutes(seconds):
    return int(seconds/60)

@register.filter(name='seconds_to_minutes_and_hours')
def seconds_to_minutes_and_hours(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    hour_string = "hours"
    minute_string = "minutes"
    if m == 1:
        minute_string = "minute"
    if h == 1:
        hour_string = "hour"
    if h:
        return "{} {} {} {}".format(h, hour_string, m, minute_string)
    else:
        return "{} {}".format(m, minute_string)

@register.filter(name='seconds_to_percentage')
def seconds_to_percentage(seconds):
    if seconds < 600:
        return int(round(seconds/600, 2)*100)
    elif seconds >= 600:
        return 100
    else:
        return 0


#=========================================================================================================
#                                              NWEA
#=========================================================================================================

@register.simple_tag(name='nwea_recommended_skills_list')
def nwea_recommended_skills_list(student, arg):
    return nwea_skills(student, arg)


@register.simple_tag(name='class_recommendation_list')
def class_recommendation_list(student_list):
    # skill_list=[]     # Need a better way to do this
    # for student in student_list:
    #     skill_list.append(nwea_skills(student, "recommended_skill_list"))
    # return skill_list
    pass





#=========================================================================================================
#                                           NAVIGATION
#=========================================================================================================


@register.inclusion_tag('brain/classes_nav.html')
def nav_classrooms_list(request):
    user = request.user
    classrooms = Classroom.objects.filter(classroomassignment__teacher=user)
    return {'classrooms': classrooms}


@register.inclusion_tag('amc/classes_nav.html')
def nav_amc_classrooms_list():
    classrooms = Classroom.objects.all().filter(currentclass__grade='2nd')
    return {'classrooms': classrooms}

@register.inclusion_tag('ixl/ixl_nav.html')
def nav_ixl_list():
    return





#=========================================================================================================
#                                           SCORE IT
#=========================================================================================================

@register.simple_tag(name='add_subject_score')
def add_subject_score(student, date, subject):
    #Get the score object
    if isinstance(date, str):
        dateobj = datetime.datetime.strptime(date, '%Y, %-m, %-d').date()
        day = dateobj.strftime('%A')
    else:
        day = date.strftime('%A')

    try:
        obj = Score.objects.get(student__student_id=student, date=date, subject__title=subject)
        x = 0

        if obj.hand:
            x += 1
        if obj.slant:
            x += 2
        if obj.transition:
            x+=2
        if obj.please:
            x += 1
        if obj.instruction:
            x += 2
        if obj.material:
            x += 1
        if obj.peer:
            x += 1
    except:
        x=None
    # If each part is True: Assign the right number of points. Add to X
    return x


@register.simple_tag(name='add_total_score')
def add_total_score(student, date):
    total=0
    # Get student obj
    student = StudentRoster.objects.get(student_id=student)
    # Given the date, find the day of the week of that date
    # get classroom
    classroom = student.current_class.classroom
    # Get Classroom's schedule
    if isinstance(date, str):
        dateobj = datetime.datetime.strptime(date, '%Y, %-m, %-d').date()
        day = dateobj.strftime('%A')
    else:
        day = date.strftime('%A')
    try:
        schedule = Schedule.objects.get(classroom=classroom, day=day.upper())
    except:
        schedule = Schedule.objects.get(classroom=classroom, day="MONDAY")
    # Get list of all classes on this day in order
    classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                  schedule.subject6, schedule.subject7]
    for subject in classes:
        answer = add_subject_score(student.student_id, date, subject)
        if answer:
            total += answer
    return total



