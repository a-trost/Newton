import datetime
import random

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from brain.models import StudentRoster, CurrentClass
from .models import CGIResult, CGI
from .forms import CGIResultsForm, CGIForm


# Create your views here.



def print_cgi(request, classroom="Trost", grade="2nd"):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__classroom__last_name=classroom)
    student_and_cgi_list = get_student_and_cgi_list(student_list)

    return render(request, 'mathcgi/cgi_print.html',
                  {'grade': grade, 'classroom': classroom, 'student_and_cgi_list': student_and_cgi_list})


# Get student list
# For each student, get their current CGI Results, sorted by CGI #
# Run through the form set




def input_cgi(request,  grade="2nd", classroom="Trost"):  # Input CGI data for whole class
    if request.method == 'POST':  # If submit was pressed and we have a post...
        InputCGIFormSet = formset_factory(CGIResultsForm, extra=0)
        formset = InputCGIFormSet(request.POST)
        has_errors = False

        for form in formset:
            # Seems like it should be possible to have the form know the instance it was created from, and update
            # that rather than go through this manual process
            if form.is_valid():
                form.save()
            else:
                existing_results = CGIResult.objects.filter(student=form.instance.student,
                                                            cgi=form.instance.cgi,
                                                            progress=form.instance.progress)
                if form.instance.progress and existing_results.count():
                    instance = existing_results.first()
                    instance.progress = form.instance.progress
                    instance.save()
                else:
                    has_errors = True
                    print(form.errors)
        messages.add_message(request, messages.SUCCESS, "CGI Results Updated!")
        if not has_errors:
            url = reverse('mathcgi:inputcgi', kwargs={'grade': grade, 'classroom': classroom})
            return HttpResponseRedirect(url)

    else:
        student_list = StudentRoster.objects.filter(first_name="Jamari")
        cgi = CGI.objects.filter(cgi_number=4)

        # cgi_result = CGIResult.objects.get(cgi=cgi, student=student)
        # data = {'student': cgi_result.student, 'cgi': cgi_result.cgi, 'progress':cgi_result.progress}
        # form = CGIResultsForm(initial=data)


        # student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        #     .filter(current_class__classroom__last_name=classroom)
        form_count = student_list.count()  # How many rows for students will there be?
        CGIListFormSet = formset_factory(CGIResultsForm, extra=form_count)
        formset = CGIListFormSet()
        # Would be nice to create forms from the instances rather than manually set initial, but that did not seem
        # to work correctly
        for i in range(form_count): # Go through the student list one at a time and get all CGI results
            existing_results = CGIResult.objects.filter(student=student_list[i]).order_by('cgi__cgi_number')
            for result in existing_results: #For each result, put them in a list
                # Then put the student and the cgi results together and add to the list you're exporting.
                pass


            instance = existing_results.first()
            formset.forms[i].instance = instance
            initial_student = instance.student
            initial_progress = instance.progress

            formset.forms[i].fields['student'].initial = initial_student
            formset.forms[i].fields['cgi'].initial = i + 1
            formset.forms[i].fields['progress'].initial = initial_progress

            # if a GET (or any other method) we'll create a blank form

    return render(request, 'mathcgi/input_cgi.html', {'student_list': student_list,
                                                      # 'cgi_list':cgi_list, 'cgi_student_list':cgi_student_list,
                                                      'grade': grade,
                                                      'classroom': classroom, 'formset': formset,
                                                       })


def get_student_and_cgi_list(student_list):
    """Function to get 1 outstanding CGI problem for each student. If student has no outstanding CGI problems,
    function will not include their name or any CGI for them.
    Gets all CGIs where the date has passed.
     Gets CGI's in numerical Order.
    """

    student_and_cgi_list = []
    previous_cgis = CGI.objects.filter(date_assigned__lte=datetime.date.today())

    for student in student_list:
        for cgi in previous_cgis:
            try:
                result = CGIResult.objects.get(student=student, cgi=cgi)
                if result.progress == "3":
                    continue
                else:
                    # Make random numbers for the problem
                    q = cgi.first_num_low
                    w = cgi.first_num_high
                    first_number = random.randrange(q, w, 1)
                    q = cgi.second_num_low
                    w = cgi.second_num_high
                    second_number = random.randrange(q, w, 1)
                    problem = str(cgi.question).replace("{{ number1 }}", str(first_number)).replace("{{ number2 }}",
                                                                                                    str(second_number))
                    student_and_cgi = (student, cgi, problem)
                    student_and_cgi_list.append(student_and_cgi)
                    break
            except:
                pass

    return student_and_cgi_list


"""
Check to see if student has solved a CGI today
If not, button is visible
solve_cgi() gives student a CGI problem
student puts in the answer and hits submit
"""


def solve_cgi(request, student):
    student = get_object_or_404(StudentRoster, pk=student)
    student_and_cgi_list = get_student_and_cgi_list([student, ])
    if request.method == "POST":

        if CGIResult.objects.filter(student=student, date_taken=datetime.date.today()).exists():
            pass
        else:
            form = CGIForm(request.POST)
            if form.is_valid():
                pass
                # Don't count the results
