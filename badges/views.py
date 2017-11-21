from django.shortcuts import render
from django.utils.timezone import now, timedelta
from django.contrib import messages


from badges.models import Sticker, StickerAssignment, Avatar
from brain.models import StudentRoster
from badges.forms import AvatarForm

# Create your views here.


def choose_avatar(request, student_id):
    '''
    Student changes their avatar, selecting only from unlocked stickers.
    '''

    date_object = now()
    student = StudentRoster.objects.get(student_id=student_id)
    earned_sticker_list = StickerAssignment.objects.filter(student=student, earned=True)  # Get earned stickers
    return_link = False
    # Process for form
    # Each Earned sticker aligns with a radio button.
    # Radio button on left, description in middle, sticker image on the right.
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AvatarForm(request.POST)
        avatar = form.save(commit=False)
        avatar.student = student
        avatar.date_selected = date_object
        avatar.sticker = Sticker.objects.get(id=request.POST['sticker'])
        avatar.save()
        messages.add_message(request, messages.SUCCESS,
                             "{} {}'s avatar saved!".format(student.first_name, student.last_name[0]))
        return_link = True
    #    return HttpResponseRedirect(avatar.get_absolute_url())

    # if a GET (or any other method) we'll create a blank form
    else:
        # Check to see if the student/subject/date object already exists. If so, get that data. Otherwise new form

        form = AvatarForm()

    return render(request, 'badges/choose_avatar.html', {
        'student_id': student_id, 'student': student, 'earned_sticker_list':earned_sticker_list,
        'form': form, 'return_link':return_link,
    })
