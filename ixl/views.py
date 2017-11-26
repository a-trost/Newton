import re

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import formset_factory, modelformset_factory
from django.db import transaction, IntegrityError

from .forms import CreateIXLListForm, IXLListExerciseForm, BaseIXLListExerciseFormSet, IXLListAssignmentModelForm

from ixl.models import IXLSkill, IXLSkillScores, IXLList, IXLListAssignment, IXLListExercise, IXLListSkill

from brain.models import StudentRoster, CurrentClass, Classroom, ClassroomAssignment
from brain.templatetags import brain_extras


def skill_detail(request, skill_id):
    skill_id = skill_id.upper()
    skill = IXLSkill.objects.all().get(skill_id=skill_id)
    return render(request, 'ixl/skill_detail.html', {'skill': skill})


def level_detail(request, level):
    skill_list = IXLSkill.objects.all().filter(skill_id__startswith=level)
    return render(request, 'ixl/level_detail.html', {'level':level, 'skill_list': skill_list})


def class_list(request, grade="2nd", classroom="Trost"):
    # url: /brain/16-17/2nd/trost
    student_list = StudentRoster.objects.filter(current_class__grade=grade)\
        .filter(current_class__classroom__last_name=classroom)
    return render(request, 'ixl/class_list.html', {'student_list': student_list, 'grade': grade,
                                                     'classroom': classroom})


# class ixl_list_create(generic.CreateView):
#     model = IXLList
#     form_class = IXLListForm
#     # fields = ['title', 'author', 'category','exercises',]


def ixl_lists(request):
    user = request.user
    classroom_assignments = ClassroomAssignment.objects.filter(teacher=user)
    classroom = []
    for classroom_assignment in classroom_assignments:
        classroom.append(classroom_assignment.classroom)

    return render(request, 'ixl/ixl_lists.html', {'classroom':classroom})

def ixl_list_create(request):
    if request.method == 'POST':
        form = CreateIXLListForm(request.POST)
        if form.is_valid():
            ixl_list = IXLList()
            ixl_list.author = request.user
            ixl_list.title = form.cleaned_data['title']
            ixl_list.category = form.cleaned_data['category']
            ixl_list.description = form.cleaned_data['description']

            ixl_list.save()
            return HttpResponseRedirect(
                '/ixl/lists/view/{}'.format(ixl_list.pk))  # Soon this will send us to the assign exercises page
    else:
        form = CreateIXLListForm()

    return render(request, 'ixl/ixl_list_create_form.html', {'form': form})


def ixl_list_exercise_assign(request, list):
    """
        Allows a user to add exercises to an IXL list.
    """
    ixl_list = get_object_or_404(IXLList, pk=list)
    user = request.user
    # Create the formset, specifying the form and formset we want to use.
    IXLListExerciseFormSet = formset_factory(IXLListExerciseForm, formset=BaseIXLListExerciseFormSet)
    # Get our existing  data for this list.  This is used as initial data.
    ixl_list_exercises = IXLListExercise.objects.filter(list=ixl_list).order_by('order')
    ixl_list_exercise_data = [
        {'grade': l.list_skill.grade, 'id_code': l.list_skill.id_code, 'required_score': l.required_score,
         'list': l.list, 'order': l.order} for l in ixl_list_exercises]

    if request.method == "POST":
        ixl_list_exercise_formset = IXLListExerciseFormSet(request.POST)
        if ixl_list_exercise_formset.is_valid():
            new_exercises = []
            for order, exercise_form in enumerate(ixl_list_exercise_formset):
                try:
                    grade = exercise_form.cleaned_data['grade']
                    id_code = exercise_form.cleaned_data['id_code']
                    required_score = exercise_form.cleaned_data['required_score']
                    if grade and id_code and required_score:
                        ixl_list_skill = IXLListSkill.objects.filter(grade=grade, id_code=id_code).first()
                        new_exercises.append(
                            IXLListExercise(list_skill=ixl_list_skill, required_score=required_score, order=order,
                                            list=ixl_list))
                except:
                    pass
            try:
                with transaction.atomic():
                    # Replace the old with the new
                    IXLListExercise.objects.filter(list=ixl_list).delete()
                    IXLListExercise.objects.bulk_create(new_exercises)

                    # And notify our users that it worked
                    messages.success(request, 'You have updated the list: {}'.format(ixl_list.title))
                    return HttpResponseRedirect('/ixl/lists/view/{}'.format(list))

            except IntegrityError:  # If the transaction failed
                messages.error(request, 'There was an error saving the list.')
                return HttpResponseRedirect('/ixl/lists/view/{}'.format(list))

    ixl_list_exercise_formset = IXLListExerciseFormSet(initial=ixl_list_exercise_data)

    context = {
        'list': ixl_list,
        'formset': ixl_list_exercise_formset,
    }
    return render(request, 'ixl/ixl_list_assign_exercises.html', context)



def view_lists(request):
    user = request.user
    # classrooms = ClassroomAssignment.objects.filter(teacher = user)
    my_ixl_lists = IXLList.objects.filter(author=user).order_by('-id')
    other_ixl_lists = IXLList.objects.exclude(author=user).order_by('-id')

    return render(request, 'ixl/view_lists.html',{'user':user, 'my_ixl_lists':my_ixl_lists,
                                                  'other_ixl_lists':other_ixl_lists})

def view_single_list(request, list):
    list = get_object_or_404(IXLList, pk=list)
    list_exercises = IXLListExercise.objects.filter(list=list).order_by('order')
    return render(request, 'ixl/view_single_list.html', {'list': list, 'list_exercises': list_exercises})


def edit_list(request, list):
    list = get_object_or_404(IXLList, pk=list)
    if request.method == 'POST':
        form = CreateIXLListForm(request.POST)
        if form.is_valid():
            ixl_list = list
            ixl_list.author = request.user
            ixl_list.title = form.cleaned_data['title']
            ixl_list.category = form.cleaned_data['category']
            ixl_list.description = form.cleaned_data['description']
            ixl_list.save()
            return HttpResponseRedirect(
                '/ixl/lists/view/{}'.format(list.pk))  # Soon this will send us to the assign exercises page
    else:
        form = CreateIXLListForm(
            initial={'title': list.title, 'category': list.category, 'description': list.description})
    return render(request, 'ixl/ixl_list_create_form.html', {'form': form, })



def delete_list(request, list):
    user = request.user
    list = get_object_or_404(IXLList, pk=list)
    if not user == list.author:
        raise Http404
    if request.method == "POST":
        messages.success(request, 'You have deleted the list: {}'.format(list.title))
        list.delete()
        return HttpResponseRedirect('/ixl/lists/view/')
    return render(request, 'ixl/ixl_list_delete.html', {'list': list})


def ixl_assign_list(request, list):
    '''
    Creates an IXLListAssignment object for current list and students in user's class.
    Sets the assigned value to True or False, and then might change the number to assign. Doesn't delete the object
    if you uncheck it.
    Gives student, ixl_list, and number_to_assign.
    '''
    user = request.user
    list = get_object_or_404(IXLList, pk=list)
    student_list = []
    ixl_list_assignments = []
    if not user == list.author:
        raise Http404
    classrooms = Classroom.objects.filter(classroomassignment__teacher=user)
    for classroom in classrooms:
        student_list = StudentRoster.objects.filter(classroom=classroom).order_by('last_name')
        for student in student_list:
            obj, created = IXLListAssignment.objects.get_or_create(student=student, ixl_list=list)
            ixl_list_assignments.append(obj)
    # Create the formset, specifying the form and formset we want to use.
    IXLListAssignmentFormSet = modelformset_factory(IXLListAssignment, form=IXLListAssignmentModelForm,
                                                    fields=['student', 'assigned', 'number_to_assign'])
    # Get our existing  data for this list.  This is used as initial data.
    ixl_list_assignment_data = [
        {'student': l.student, 'ixl_list': list, 'assigned': l.assigned,
         'date_created': l.date_created, 'number_to_assign': l.number_to_assign} for l in ixl_list_assignments]

    ixl_list_assignment_formset = IXLListAssignmentFormSet(initial=ixl_list_assignment_data)  # A list of dictionaries
    context = {
        'list': list,
        'formset': ixl_list_assignment_formset,
    }
    return render(request, 'ixl/ixl_list_assign.html', context)
