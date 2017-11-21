from django.shortcuts import render
from brain.models import StudentRoster, CurrentClass, Classroom, Schedule, Subject
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Score, TeacherApproval
from .forms import ScoreForm
import datetime
from django.utils.timezone import now, timedelta
from brain.templatetags.brain_extras import add_total_score
from variables import SUBJECTDICT, STYLEDICT


def class_list(request, student_id):
    # Get the Day
    date_object = datetime.date.today()
    day = date_object.strftime("%A")
    # Get student
    student = StudentRoster.objects.get(student_id=student_id)
    # Get student's classroom
    classroom = student.current_class.classroom
    # Get student's classroom's schedule for this day
    grade = student.current_class.grade
    try:
        schedule = Schedule.objects.get(classroom=classroom, day=day.upper())
    except:
        schedule = Schedule.objects.get(classroom=classroom, day="MONDAY")
    # Get list of all classes on this day in order
    classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
               schedule.subject6, schedule.subject7]
    classesandstyles = []
    for item in classes:  # Item = reading or writing
        # Find out if there is a score for the subject yet, and if so, put the score. Otherwise return None.
        icon, color = STYLEDICT[item.title]
        classesandstyles.append((item, icon, color))

    return render(request, 'scoreit/class_list.html', {'classesandstyles': classesandstyles, 'student': student,
                                                       'classroom': classroom, 'day': day, 'schedule': schedule,

                                                       'grade': grade, 'date': date_object,
                                                       })


def log_subject(request, student_id, subject):
    '''For this I need to have the different criteria in order for that subject. At the top it will say "CHANZE'S SPANISH SCORE IT"
    and it'll have the criteria with yes/no going down, with a submit button at the bottom. If they have already submitted the form
    it will be the same scores from before. If this is the first time, they will get a blank form where they have to click yes/no
    When they hit submit, it either creates or updates the form. '''
    # Get the Day
    date_object = now()
    day = date_object.strftime("%A")
    # Get student
    student = StudentRoster.objects.get(student_id=student_id)
    subjectobj = Subject.objects.get(title=subject)
    descriptions = SUBJECTDICT[subject]
    obj, created = Score.objects.get_or_create(student=student, date=date_object, subject=subjectobj)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ScoreForm(request.POST, instance=obj)
        score = form.save(commit=False)
        score.subject = subjectobj
        score.student = student
        score.date = date_object
        score.save()
        messages.add_message(request, messages.SUCCESS,
                             "{} score saved!".format(subject))
        return HttpResponseRedirect(score.get_absolute_url())

    # if a GET (or any other method) we'll create a blank form
    else:
        # Check to see if the student/subject/date object already exists. If so, get that data. Otherwise new form
        form = ScoreForm(instance=obj)

    return render(request, 'scoreit/log_subject.html', {
        'student_id': student_id, 'student': student,
        'subject': subject, 'form': form, 'descriptions': descriptions
    })


def grade_view(request):
    classroom_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    weekend = ['SATURDAY', 'SUNDAY']
    if day_of_week.upper() in weekend:
        day_of_week = "Friday"
    classroom_student_list = []
    for classroom in classroom_list:
        classroomobj = Classroom.objects.get(last_name=classroom)
        schedule = Schedule.objects.get(classroom=classroomobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__classroom__last_name=classroom).order_by('first_name')
        classroom_student_list.append((classroom,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'classroom_student_list':classroom_student_list, 'date':date_object,
    })

def grade_view_yesterday(request):
    classroom_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(days=1) - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    classroom_student_list = []
    for classroom in classroom_list:
        classroomobj = Classroom.objects.get(last_name=classroom)
        schedule = Schedule.objects.get(classroom=classroomobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__classroom__last_name=classroom).order_by('first_name')
        classroom_student_list.append((classroom,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'classroom_student_list':classroom_student_list, 'date':date_object,
    })

def grade_view_twodays(request):
    classroom_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(days=2) - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    classroom_student_list = []
    for classroom in classroom_list:
        classroomobj = Classroom.objects.get(last_name=classroom)
        schedule = Schedule.objects.get(classroom=classroomobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__classroom__last_name=classroom).order_by('first_name')
        classroom_student_list.append((classroom,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'classroom_student_list':classroom_student_list, 'date':date_object,
    })
def grade_view_threedays(request):
    classroom_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(days=3) - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    classroom_student_list = []
    for classroom in classroom_list:
        classroomobj = Classroom.objects.get(last_name=classroom)
        schedule = Schedule.objects.get(classroom=classroomobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__classroom__last_name=classroom).order_by('first_name')
        classroom_student_list.append((classroom,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'classroom_student_list':classroom_student_list, 'date':date_object,
    })