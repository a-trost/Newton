import re

from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .forms import CreateIXLListForm


from ixl.models import IXLSkill, IXLSkillScores, IXLList, IXLListAssignment
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
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = CreateIXLListForm(request.POST)
        if form.is_valid():
            ixl_list = IXLList()
            ixl_list.author = request.user
            ixl_list.title = form.cleaned_data['title']
            ixl_list.category = form.cleaned_data['category']
            ixl_list.save()
            return HttpResponseRedirect('/ixl/lists/view/')
    else:
        form = CreateIXLListForm()

    return render(request, 'ixl/ixl_list_create_form.html', {'form': form})


def view_lists(request):
    user = request.user
    # classrooms = ClassroomAssignment.objects.filter(teacher = user)
    my_ixl_lists = IXLList.objects.filter(author=user).order_by('-id')
    other_ixl_lists = IXLList.objects.exclude(author=user).order_by('-id')

    return render(request, 'ixl/view_lists.html',{'user':user, 'my_ixl_lists':my_ixl_lists,
                                                  'other_ixl_lists':other_ixl_lists})

def view_single_list(request, list):
    list = get_object_or_404(IXLList, pk=list)
    return render(request, 'ixl/view_single_list.html', {'list':list,})