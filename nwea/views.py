import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from . import forms
from brain.models import StudentRoster, CurrentClass
from brain.templatetags import brain_extras
from .models import NWEAScore, RITBand


@login_required
def input_nwea_scores(request, season="Fall",  grade="2nd", classroom="Trost"):
    if request.method == 'POST':
        TestListFormSet = formset_factory(forms.InputNWEAScores, extra=0)
        formset = TestListFormSet(request.POST)
        has_errors = False
        for form in formset:
            # Seems like it should be possible to have the form know the instance it was created from, and update
            # that rather than go through this manual process
            if form.is_valid():
                form.save()
            else:
                existing_results = NWEAScore.objects.filter(student=form.instance.student,

                                                            season=form.instance.season,)
                if form.instance.subdomain1 and existing_results.count():
                    instance = existing_results.first()
                    instance.subdomain1 = form.instance.subdomain1
                    instance.save()
                else:
                    has_errors = True
                    print(form.errors)
        messages.add_message(request, messages.SUCCESS, "NWEA Scores Recorded!")
        if not has_errors:
            url = reverse('brain:classlist', kwargs={ 'grade': grade, 'classroom': classroom})
            return HttpResponseRedirect(url)
    else:
        student_list = StudentRoster.objects.filter(current_class__grade=grade) \
            .filter(current_class__classroom__last_name=classroom)

        form_count = student_list.count()
        TestListFormSet = formset_factory(forms.InputNWEAScores, extra=form_count)
        formset = TestListFormSet()
        # Would be nice to create forms from the instances rather than manually set initial, but that did not seem
        # to work correctly
        for i in range(form_count):
            #today = datetime.date.today()
            #existing_results = NWEAScore.objects.filter(student=student_list[i], test_date=today)
            # if existing_results.count():
            #     instance = existing_results.first()
            #     formset.forms[i].instance = instance
            #     initial_student = instance.student
            #     initial_subdomain1 = instance.subdomain1
            #     initial_subdomain2 = instance.subdomain2
            #     initial_subdomain3 = instance.subdomain3
            #     initial_subdomain4 = instance.subdomain4
            #     initial_subdomain5 = instance.subdomain5
            #     initial_subdomain6 = instance.subdomain6
            #     initial_subdomain7 = instance.subdomain7
            #     initial_subdomain8 = instance.subdomain8
            #
            #
            # else:
            initial_student = student_list[i]
            initial_subdomain1 = None
            initial_subdomain2 = None
            initial_subdomain3 = None
            initial_subdomain4 = None
            initial_subdomain5 = None
            initial_subdomain6 = None
            initial_subdomain7 = None
            initial_subdomain8 = None


            formset.forms[i].fields['student'].initial = initial_student
            formset.forms[i].fields['subdomain1'].initial = initial_subdomain1
            formset.forms[i].fields['subdomain2'].initial = initial_subdomain2
            formset.forms[i].fields['subdomain3'].initial = initial_subdomain3
            formset.forms[i].fields['subdomain4'].initial = initial_subdomain4
            formset.forms[i].fields['subdomain5'].initial = initial_subdomain5
            formset.forms[i].fields['subdomain6'].initial = initial_subdomain6
            formset.forms[i].fields['subdomain7'].initial = initial_subdomain7
            formset.forms[i].fields['subdomain7'].initial = initial_subdomain8


    context = {
        'formset': formset,
        'classroom': classroom,
        'grade': grade,

    }
    return render(request, 'nwea/input_nwea_scores_form.html', context=context)
