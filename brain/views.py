from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
import random
from datetime import date, timedelta, datetime, timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView



from .models import StudentRoster, Classroom, CurrentClass, AccountInfo, MorningMessage, MorningMessageSettings, Schedule, \
    ClassroomAccountPassword, AttendanceLog, AttendanceAlert, ClassroomAssignment
from amc.models import AMCTestResult
from ixl.models import IXLSkillScores, IXLStats, Challenge, ChallengeAssignment, ChallengeExercise, IXLSkill, IXLTimeSpent
from libs.functions import nwea_recommended_skills_list, class_skills_list
from brain.models import ReadingStats, ReadingTimeSpent
from .forms import PasswordForm
from badges.models import Sticker, StickerAssignment, Avatar
from brain.forms import MorningMessageForm
from brain.templatetags.brain_extras import challenges_completed
from .models import DataUpdate
from variables import *

today = date.today()

@login_required
def class_list(request, grade="2nd", classroom="Trost"):
    # url: /brain/17-18/2nd/trost
    classroom_object = Classroom.objects.get(last_name=classroom)

    current_date = date.today() - timedelta(hours=5)
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__classroom__last_name=classroom)

    ## Start Reading Statistics ##
    reading_list = ReadingStats.objects.filter(student__current_class__classroom=classroom_object).order_by(
        'student__last_name')

    total_starting_lexile, total_current_lexile, total_lexile_progress, total_myon_time_spent, total_lexile_goal = 0, 0, 0, 0, 0
    for item in reading_list:
        if item.starting_lexile:
            total_starting_lexile += item.starting_lexile
        if item.current_lexile:
            total_current_lexile += item.current_lexile
        if item.lexile_progress:
            total_lexile_progress += item.lexile_progress
        if item.goal_lexile:
            total_lexile_goal += item.goal_lexile
        if item.myon_time_spent:
            total_myon_time_spent += item.myon_time_spent

    class_size = len(student_list)
    if class_size:
        reading_averages = [round(total_starting_lexile / class_size), round(total_current_lexile / class_size),
                        round(total_lexile_progress / class_size), round(total_lexile_goal / class_size),
                        round(total_myon_time_spent / class_size)]
    else:
        reading_averages = 0

    ixl_priority = IXLStats.objects.filter(student__current_class__classroom=classroom_object).order_by('time_spent')
    myon_priority = reading_list.order_by('myon_time_spent')

    ## End Reading Statistics

    ## Start IXL Challenge ##
    challenge_list = []
    for student in student_list:
        try:
            challenge = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
        except ChallengeAssignment.DoesNotExist:
            challenge,progress = None,None
        if challenge:
            total_complete, total_questions = challenge.completed()
        challenge_list.append((challenge, total_complete, total_questions))

    ## End IXL Challenge ##

    ##-------------------------START CBA GRID-----------------------##


    spring_cba_student_grid = []
    for student in student_list:
        studentname = "{} {}.".format(student.first_name, student.last_name[0])
        ixl_score_list = [studentname, ]
        for i in range(20):  # Go through each exercise and get the score
            if spring_cba_ixl_match[i] != None:
                try:
                    score = IXLSkillScores.objects.get(student_id=student,
                                                       ixl_skill_id__skill_id=spring_cba_ixl_match[i])
                    score = score.score
                except:
                    score = 0
            else:
                score = None
            ixl_score_list.append(score)  # Append the score on the score list
        spring_cba_student_grid.append(ixl_score_list)  # when all done, append the score list and go to next student
    last_cba_row = ["IXL:"]
    for i in spring_cba_ixl_match:
        last_cba_row.append(i)

    #last_cba_row = [("IXL:",), spring_cba_ixl_match]
    #last_cba_row.insert(0, "IXL:")
    spring_cba_student_grid.append(last_cba_row)

    ##-------------------------END CBA GRID-----------------------##

    last_updated = DataUpdate.objects.first()

    return render(request, 'brain/class_list.html', {'student_list': student_list, 'grade': grade,
                                                     'classroom': classroom, 'classroom_object': classroom_object,
                                                     'reading_list': reading_list,
                                                     'challenge_list': challenge_list,
                                                     'reading_averages': reading_averages, 'ixl_priority': ixl_priority,
                                                     'myon_priority': myon_priority,
                                                     'spring_cba_student_grid': spring_cba_student_grid,
                                                     'spring_cba_descriptions': spring_cba_descriptions,
                                                     'spring_cba_ixl_match': spring_cba_ixl_match,
                                                     'last_updated':last_updated

                                                     })

@login_required
def student_detail(request, studentid, ):  # Look at a single student's record
    # url: /student/83
    amc_tests = AMCTestResult.objects.all().filter(student_id=studentid)[:5]
    ixl_scores = IXLSkillScores.objects.all().filter(student_id=studentid)
    student = get_object_or_404(StudentRoster, student_id=studentid)
    actual_nwea_scores, estimated_nwea_scores, recommended_skill_list, subdomain_percentage_complete = nwea_recommended_skills_list(
        student, "all")
    return render(request, 'brain/student_detail.html', {'student': student, 'amc_tests': amc_tests,
                                                         'ixl_scores': ixl_scores,
                                                         "actual_nwea_scores": actual_nwea_scores,
                                                         "estimated_nwea_scores": estimated_nwea_scores,
                                                         "recommended_skill_list": recommended_skill_list,
                                                         "subdomain_percentage_complete": subdomain_percentage_complete})

def index(request):
    try:
        if request.user.is_authenticated:
            if request.user.first_name != "":
                user_name = request.user.first_name
            else:
                user_name = request.user.username
        else:
            user_name=None
    except:
        user_name = None


    return render(request, 'brain/index.html',{'user_name': user_name} )


def portal_school(request):  # Portal that lists all the classrooms in the school
    class_list = CurrentClass.objects.order_by('classroom', )
    school_ixl_time_spent = IXLStats.objects.all().order_by('-time_spent')[:10]
    reading_stats = ReadingStats.objects.all()
    school_myon_time_spent = reading_stats.order_by('-myon_time_spent')[:10]
    school_myon_lexile_progress = reading_stats.order_by('-lexile_progress').exclude(lexile_progress__isnull=True)[:10]

    return render(request, 'brain/portal_school.html', {'class_list': class_list, 'color_list': COLORS,
                                                        'icon_list': ICONS, 'school_ixl_time_spent':
                                                            school_ixl_time_spent,
                                                        'school_myon_time_spent': school_myon_time_spent,
                                                        'school_myon_lexile_progress': school_myon_lexile_progress, })


def portal_class(request, classroom="Trost", grade="2nd"):  # Portal that lists all the students in that class
    # Get Student List
    today = date.today()
    display_dict = {'ixl':False,'myon':False,'ixl_challenge':False,'avatar':False}
    # TODO: Figure out if the class has IXL Time Data, Myon Time Data, and IXL Challenges
    # TODO: If it has each of those, send a dict through. The template will display 1, 2, or 3 of the modules
    if ClassroomAccountPassword.objects.filter(classroom__last_name__contains=classroom).filter(site__icontains="IXL").exists():
        display_dict['ixl'] = True
    if ClassroomAccountPassword.objects.filter(classroom__last_name__contains=classroom).filter(site__icontains="MYON").exists():
        display_dict['myon'] = True



    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__classroom__last_name=classroom).order_by('first_name')

    classroom = Classroom.objects.get(last_name=classroom)
    # Sort the student list by their number of IXL minutes spent [:5]
    class_ixl_time_spent = IXLTimeSpent.objects.filter(student__classroom=classroom).filter(date_spent=datetime.today())

    class_ixl_questions_answered = IXLStats.objects.filter(student__current_class__classroom=classroom).order_by(
        '-questions_answered')[:5]
    reading_stats = ReadingStats.objects.all()
    class_myon_lexile_progress = reading_stats.filter(student__current_class__classroom=classroom).order_by(
        '-lexile_progress').exclude(lexile_progress__isnull=True)[:5]
    # class_myon_time_spent = class_myon_time_spent[:5]
    # class_myon_books_read = class_myon_books_read[:5]
    leaderboardclassrooms = ['Trost', 'McPherson', 'Palermo', 'Mackinnon' ]
    myon_leaderboardclassrooms = ['Trost', 'McPherson', 'Palermo', 'Mackinnon']
    avatar_list = []
    ixl_time_spent_list = []
    myon_time_spent_list = []
    ixl_challenge_list_complete = []
    ixl_challenge_list_total=[]

    if classroom.grade == '2nd':
        display_dict['avatar'] = True
    for student in student_list:
        try:
            current_avatar = Avatar.objects.filter(student=student).latest('date_selected')
            avatar_list.append(current_avatar.sticker.image)
        except:
            avatar_list.append('static/images/stickers/blankperson.png')
        try:
            student_ixl_time = IXLTimeSpent.objects.filter(student=student).filter(date_spent=today).first()
            ixl_time_spent_list.append(student_ixl_time.rewarded_time_total())
        except:
            ixl_time_spent_list.append(0)

        # Student Myon Time spent
        try:
            student_myon_time = ReadingTimeSpent.objects.filter(student=student).filter(date_spent=today).first()
            myon_time_spent_list.append(student_myon_time.time_spent)
        except:
            myon_time_spent_list.append(0)

        # Student IXL Challenges
        try:
            student_challenge_status = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
            total_complete, total_questions = student_challenge_status.completed()
            ixl_challenge_list_complete.append(total_complete)
            ixl_challenge_list_total.append(total_questions)
            display_dict['ixl_challenge'] = True
        except:
            ixl_challenge_list_complete.append('-')
            ixl_challenge_list_total.append('-')
    class_myon_time_spent = 0
    class_ixl_time_spent = 0
    for item in myon_time_spent_list:
        class_myon_time_spent += item
    for item in ixl_time_spent_list:
        class_ixl_time_spent += item
    if classroom.last_name in leaderboardclassrooms:
        leaderboard_display = True
    else:
        leaderboard_display = False
    if classroom.last_name in myon_leaderboardclassrooms:
        myon_leaderboard_display = True
    else:
        myon_leaderboard_display = False
    return render(request, 'brain/portal_class.html', {'student_list': student_list, 'classroom': classroom, 'grade': grade,
                                                       'color_list': COLORS, 'icon_list': ICONS,
                                                       'ixl_time_spent_list': ixl_time_spent_list,
                                                       'leaderboard_display':leaderboard_display,
                                                       'class_ixl_questions_answered':class_ixl_questions_answered,
                                                       'class_myon_time_spent':class_myon_time_spent,
                                                       'class_ixl_time_spent':class_ixl_time_spent,
                                                       'class_myon_lexile_progress': class_myon_lexile_progress,
                                                       'myon_leaderboard_display': myon_leaderboard_display,
                                                       'avatar_list': avatar_list,
                                                       'myon_time_spent_list':myon_time_spent_list,
                                                        'ixl_challenge_list_complete':ixl_challenge_list_complete,
                                                       'ixl_challenge_list_total':ixl_challenge_list_total,
                                                        'display_dict':display_dict,
                                                       })




def portal_student(request, classroom, grade,
                   studentid):  # Portal that lists the student's information and provides links to the sites
    student = get_object_or_404(StudentRoster, student_id=studentid)
    settings_dict = {} #Turns on or off all features. Putting it in one condensed place
    today = date.today()

    # Get the last 4 days and put them in a list
    last_5_days = [today,]
    day_names = ["Today",]
    for d in range(1,5):
        day = (today - timedelta(days=d))
        last_5_days.append(day)
        day_names.append(day.strftime('%a'))
    last_5_days.reverse()
    day_names.reverse()
    # Determine whether we show stars for IXL and myon, or just one
    # If time stats exist, add to a setting dictionary
    if IXLTimeSpent.objects.filter(student=student).exists():
        settings_dict['ixl_time'] = True
    else:
        settings_dict['ixl_time'] = False
    if ReadingTimeSpent.objects.filter(student=student).exists():
        settings_dict['myon_time'] = True
    else:
        settings_dict['myon_time'] = False
    #  Time Spent for today and past 4 days
    ixl_time_spent = []
    myon_time_spent = []
    for day in last_5_days:
        try:
            student_ixl_time = IXLTimeSpent.objects.filter(student=student).filter(date_spent=day).first()
            ixl_time_spent.append(student_ixl_time.rewarded_time_total())
        except:
            ixl_time_spent.append(0)

        try:
            student_myon_time = ReadingTimeSpent.objects.filter(student=student).filter(date_spent=day).first()
            myon_time_spent.append(student_myon_time.time_spent)
        except:
            myon_time_spent.append(0)

    # Get total IXL and MYON Star count
    grade = student.classroom.grade
    try:
        if grade == 'K':
            ixl_star_total = IXLTimeSpent.objects.filter(student=student).filter(bTime__gte=600).count()
        elif grade == '1st':
            ixl_star_total = IXLTimeSpent.objects.filter(student=student).filter(cTime__gte=600).count()
        elif grade == '2nd':
            ixl_star_total = IXLTimeSpent.objects.filter(student=student).filter(dTime__gte=600).count()
        elif grade == '3rd':
            ixl_star_total = IXLTimeSpent.objects.filter(student=student).filter(eTime__gte=600).count()
        elif grade == '4th':
            ixl_star_total = IXLTimeSpent.objects.filter(student=student).filter(fTime__gte=600).count()
        elif grade == '5th':
            ixl_star_total = IXLTimeSpent.objects.filter(student=student).filter(gTime__gte=600).count()
        elif grade == '6th':
            ixl_star_total = IXLTimeSpent.objects.filter(student=student).filter(hTime__gte=600).count()
    except:
        ixl_star_total = 0

    try:
        myon_star_total = ReadingTimeSpent.objects.filter(student=student).filter(time_spent__gte=600).count()
    except:
        myon_star_total = 0

    # Get IXL and MYON streak count
    # If yesterday's time > 600
    # add 1 to streak and go back a day.
    ixl_streak = 0
    myon_streak = 0
    try:
        time_spent_object = IXLTimeSpent.objects.filter(student=student).filter(
            date_spent=(today)).first()
        if time_spent_object.time_goal_met() == True:
            ixl_streak += 1
        else:
            pass
    except:
        pass
    try:
        time_spent_object = ReadingTimeSpent.objects.filter(student=student).filter(
            date_spent=(today)).first()
        if time_spent_object.time_spent >= 600:
            myon_streak += 1
        else:
            pass
    except:
        pass
    for i in range(1,300):
        try:
            time_spent_object = IXLTimeSpent.objects.filter(student=student).filter(date_spent=(today - timedelta(days=i))).first()
            if time_spent_object.time_goal_met() == True:
                ixl_streak +=1
            else:
                break
        except:
            break
    for i in range(1, 300):
        try:
            time_spent_object = ReadingTimeSpent.objects.filter(student=student).filter(
                date_spent=(today - timedelta(days=i))).first()
            if time_spent_object.time_spent >= 600:
                myon_streak += 1
            else:
                break
        except:
            break
    #
    # if myon_streak > 5:
    #     messages.success(request, 'Wow, you have a myON Streak of {}. Keep it going!'.format(myon_streak))
    #
    # if ixl_streak > 5:
    #     messages.success(request, "Incredible! You have an IXL Streak of {}. Don't stop now!".format(ixl_streak))


    myon_feedback = [None, 'owl.svg', 0,0]
    try:
        accountinfo = AccountInfo.objects.get(student=student)
    except:
        accountinfo = False
    try:
        readingstats = ReadingStats.objects.get(student=student)
    except:
        readingstats = False
    if readingstats:
        if readingstats.myon_quizzes_taken < 3:
            myon_feedback = ["Hmm, you haven't taken enough myON quizzes this week. Take some and I'll let you know how you're doing, {}!".format(student.first_name),'owl-question.svg']
        elif readingstats.myon_quiz_average < .4:
            myon_feedback = [
            "Oh no, ! It doesn't seem you're trying your hardest on these quizzes. Read the book carefully, and then read each question twice!".format(student.first_name),
            'owl-question.svg']
        elif readingstats.myon_quiz_average < .6:
            myon_feedback = [
            "You're getting there, {}, but you can get above 70! Double check your answers before finishing your next quiz!".format(student.first_name),
            'owl.svg']
        elif readingstats.myon_quiz_average < .7:
            myon_feedback = [
            "Keep at it, {}! Make sure you're always asking yourself questions as you read. That's what good readers do!".format(student.first_name),
            'owl.svg']
        elif readingstats.myon_quiz_average < .85 and readingstats.myon_quizzes_taken <5:
            myon_feedback = [
            "Fantastic, {}! You've taken a couple quizzes and you've done well. Keep taking even more quizzes and I'll be super impressed!".format(student.first_name),
            'owl-hat.svg']
        elif readingstats.myon_quiz_average < .85:
            myon_feedback = [
            "Incredible, {}! You've done so well on so many quizzes this week! I LOVE how carefully you're reading those books!".format(student.first_name),
            'owl-heart.svg']
        elif readingstats.myon_quiz_average > .85 and readingstats.myon_quizzes_taken <5:
            myon_feedback = [
            "What a great start, {}! You've taken a couple quizzes and you've done so well. Keep taking quizzes and rock it all week!".format(student.first_name),
            'owl-hat.svg']
        elif readingstats.myon_quiz_average > .85:
            myon_feedback = [
            "Simply Amazing, {}! I LOVE how hard you're working on all these quizzes. You just can't be stopped!".format(student.first_name),
            'owl-heart.svg']

        myon_feedback.append(round(readingstats.myon_quiz_average * 100))
        myon_feedback.append(readingstats.myon_quizzes_taken)

    try:
        ixlstats = IXLStats.objects.get(student=student)
        if ixlstats.last_practiced == -1:
            ixlstats = False
        elif ixlstats.last_practiced == 0:
            ixlstats.last_practiced = "Today"
        elif ixlstats.last_practiced == 1:
            ixlstats.last_practiced = "Yesterday"
        elif ixlstats.last_practiced > 1:
            ixlstats.last_practiced = "{} Days Ago".format(ixlstats.last_practiced)
    except:
        ixlstats = False

    ####---------------------IXL CHALLENGE-------------------------------####

    try:
        ixl_challenge_assignment = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
    except:
        ixl_challenge_assignment = False
    bonus_exercise_list = []
    if ixl_challenge_assignment:  # get challenge
        challenge_exercise_list = []  # [(id, description, score), ]
         # [(id, description, score), ]
        current_ixl_challenge = ixl_challenge_assignment.challenge
        exercise_list = ChallengeExercise.objects.filter(challenge=current_ixl_challenge).order_by(
            '-required_score')  # Get the related exercises
        for exercise in exercise_list:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student,
                                                            ixl_skill_id__skill_id=exercise.exercise_id).score
            except:
                exercise_score = 0
            exercise_description = IXLSkill.objects.get(skill_id=exercise.exercise_id)
            if exercise.bonus:
                bonus_exercise_list.append(
                    (exercise.exercise_id, exercise_description, exercise_score, exercise.required_score))
            elif not exercise.bonus:
                challenge_exercise_list.append(
                    (exercise.exercise_id, exercise_description, exercise_score, exercise.required_score))

            # Get scores for each challenge
        total_complete, total_questions = ixl_challenge_assignment.completed()
    else:
        challenge_exercise_list = None
        current_ixl_challenge = None
        total_complete, total_questions = None, None



    ####---------------------END IXL CHALLENGE-------------------------------####

    ####---------------------START LEXILE COUNTDOWN-------------------------------####
    lexile_challenge_dates = [ '2017/10/19', '2017/11/02', '2017/11/16', '2017/11/30' ]
    lexile_countdown = True
    todays_date = datetime.today().day
    for x in lexile_challenge_dates:
        scheduled_date = datetime.strptime(x, "%Y/%m/%d").day
        if todays_date > scheduled_date:
            continue
        else:
            lexile_countdown = abs(scheduled_date - todays_date)
            break

    ####---------------------END LEXILE COUNTDOWN-------------------------------####

    ####---------------------STICKERS-------------------------------####
    # Get Current Avatar
    try:
        current_avatar = Avatar.objects.filter(student=student).latest('date_selected')
    except:
        current_avatar = False
    # See if Avatar was set more than 6 days ago
    if current_avatar:
        if abs(datetime.now(timezone.utc) - current_avatar.date_selected) >= timedelta(days=5):
            new_avatar_choice = True
        else:
            new_avatar_choice = False
    else:
        new_avatar_choice = True

    # Get full list of Stickers in a clean order
    # Get list of stickers this student has earned
    full_sticker_list = Sticker.objects.all()
    sticker_list = []
    current_category = ''
    category_list = []
    has_earned = True
    try:
        earned_sticker_list = StickerAssignment.objects.filter(student=student, earned=True)  # Get earned stickers
        for sticker in full_sticker_list:  # Iterate through all stickers
            if sticker.category == current_category:  # If the category hasn't changed from the last sticker
                if sticker.category == "Weekend Wiz Kid" or sticker.category == "Assessment Awards":
                    pass
                elif not has_earned:
                    continue
            else:
                current_category = sticker.category
                sticker_list.append(['title', sticker.category])
                has_earned = True
            try:
                earned_sticker = StickerAssignment.objects.get(student=student, sticker=sticker)
                sticker_list.append([sticker.name, sticker.slug, sticker.description, sticker.image, sticker.alt_text])
            except:
                sticker_list.append(
                    [sticker.name, sticker.slug, sticker.description, 'static/images/stickers/blanksticker.png', ''])
                has_earned = False


    except:
        earned_sticker_list = []

    ####---------------------END STICKERS-------------------------------####


    if student.classroom.grade == 'K' or student.classroom.grade == '1st':
        myon_display = False
        kids_az_display = True
    else:
        myon_display = True
        kids_az_display = False

    try:
        if readingstats.current_lexile <= 0:
            readingstats.current_lexile = "BR"
    except:
        pass
    try:
        if readingstats.starting_lexile and readingstats.current_lexile and readingstats.goal_lexile:
            lexile_goal_percentage = round((readingstats.current_lexile - readingstats.starting_lexile) / (
                readingstats.goal_lexile - readingstats.starting_lexile) * 100)
            lexile_goal_percentage = int(lexile_goal_percentage)
        else:
            lexile_goal_percentage = 0
    except:
        lexile_goal_percentage = 0
    lexile_goal_float = str(lexile_goal_percentage) + "%"

    greeting = random.choice(GREETINGS)

    return render(request, 'brain/portal_student.html', {'student': student, 'accountinfo': accountinfo,
                                                         'classroom': classroom, 'grade': grade, 'greeting': greeting,
                                                         'readingstats': readingstats, 'ixlstats': ixlstats,
                                                         'myon_display': myon_display,
                                                         'lexile_goal_percentage': lexile_goal_percentage,
                                                         'lexile_goal_float': lexile_goal_float,
                                                         'challenge_exercise_list': challenge_exercise_list,
                                                         'current_ixl_challenge': current_ixl_challenge,
                                                         'ixl_challenge_assignment': ixl_challenge_assignment,
                                                         'second_classrooms': second_classrooms,
                                                         'total_complete':total_complete,
                                                         'total_questions':total_questions,
                                                         # 'ixl_challenge_status': ixl_challenge_status,
                                                         # 'extra_challenge_threshold': extra_challenge_threshold,
                                                         'bonus_exercise_list': bonus_exercise_list,
                                                         'earned_sticker_list': earned_sticker_list,
                                                         'sticker_list': sticker_list,
                                                         'new_avatar_choice': new_avatar_choice,
                                                         'current_avatar': current_avatar,
                                                         'lexile_countdown': lexile_countdown,
                                                         'myon_time_spent':myon_time_spent,
                                                         'ixl_time_spent':ixl_time_spent,
                                                         'day_names':day_names,
                                                         'ixl_star_total':ixl_star_total,
                                                        'myon_star_total':myon_star_total,
                                                         'myon_streak':myon_streak,
                                                         'ixl_streak':ixl_streak,
                                                         'kids_az_display':kids_az_display,
                                                            'myon_feedback':myon_feedback,
                                                         })

def timer(request):
    return render(request, 'brain/timer.html',
                  {})


def make_groups(request, grade, classroom):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__classroom__last_name=classroom)
    partner_list = []
    for student in student_list:
        partner_list.append(student.first_name)
    random.shuffle(partner_list)
    final_list = []
    classroom = Classroom.objects.get(last_name=classroom)
    if len(partner_list) % 2 == 0:  # Even
        while len(partner_list) > 0:
            try:
                partnership = partner_list.pop(0) + " + " + partner_list.pop(0)
                final_list.append(partnership)
            except:
                break
    else:  # Odd
        partnership = partner_list.pop(0) + " + " + partner_list.pop(0) + " + " + partner_list.pop(0)
        final_list.append(partnership)
        while len(partner_list) > 0:
            try:
                partnership = partner_list.pop(0) + " + " + partner_list.pop(0)
                final_list.append(partnership)
            except:
                break
    return render(request, 'brain/make_groups.html',
                  {'partner_list': final_list, 'color_list': COLORS, 'classroom': classroom})

def toolkit(request, grade, classroom):
    classroom = Classroom.objects.filter(last_name__contains=classroom).first()
    return render(request, 'brain/toolkit.html',
                  {'grade':grade, 'classroom': classroom, })


def pledge(request):
    return render(request, 'brain/pledge.html',{})

def music(request):
    return render(request, 'brain/music.html',{})


def random_student(request, grade, classroom):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__classroom__last_name=classroom)
    if student_list:
        student = random.choice(student_list)
        student = student.first_name
    else:
        student = "No Students!"
    color = random.choice(COLORS)
    return render(request, 'brain/random_student.html',
                  {'student': student, 'color_list': COLORS, 'classroom': classroom, 'color': color})


def morning_message(request, grade, classroom):
    date_object = date.today()  # Set the date to today
    try:  # See if there is a morning message for today.
        message = MorningMessage.objects.all().get(classroom__last_name=classroom, date=date_object)
    except:  # If not, just leave it as ""
        message = ""
    todays_date = date_object.strftime("%A, %B %e, %Y")  # Format the date

    try:  # Get the Morning Message settings for that classroom
        all_morning_message_settings = MorningMessageSettings.objects.get(classroom__last_name__contains=classroom)
        ending_comment = all_morning_message_settings.endingcomment
        DAY_DICT = {"Monday": (all_morning_message_settings.specialsmonday, all_morning_message_settings.box1monday),
                    "Tuesday": (all_morning_message_settings.specialstuesday, all_morning_message_settings.box1tuesday),
                    "Wednesday": (all_morning_message_settings.specialswednesday, all_morning_message_settings.box1wednesday),
                    "Thursday": (all_morning_message_settings.specialsthursday, all_morning_message_settings.box1thursday),
                    "Friday": (all_morning_message_settings.specialsfriday, all_morning_message_settings.box1friday),
                    "Saturday": (all_morning_message_settings.specialsfriday, all_morning_message_settings.box1friday),
                    "Sunday": (all_morning_message_settings.specialsmonday, all_morning_message_settings.box1monday), }
        specials,box1 = DAY_DICT[date_object.strftime("%A")][0], DAY_DICT[date_object.strftime("%A")][1]

    except:
        all_morning_message_settings = None
        ending_comment = "Sincerely,"
        specials = None
        box1 = None

    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(classroom__last_name=classroom)

    challenge_list = []
    for student in student_list:
        try:
            challenge = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
            total_complete, total_questions = challenge.completed()
            challenge_list.append((challenge, total_complete, total_questions))
        except:
            pass


    return render(request, 'brain/morning_message.html', {'classroom': classroom, 'grade': grade,
                                                          'todays_date': todays_date, 'message': message,
                                                          'specials': specials, 'box1': box1,
                                                          'all_morning_message_settings': all_morning_message_settings,
                                                          'challenge_list': challenge_list,'ending_comment':ending_comment })


def password(request, grade, classroom, studentid):
    # if this is a POST request we need to process the form data
    try:
        password_on_file = AccountInfo.objects.get(student__student_id=studentid).myonpass
    except:
        password_on_file = "admin"
    student = StudentRoster.objects.get(student_id=studentid)
    current_class = student.current_class
    grade = current_class.grade
    classroom = current_class.classroom
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data['password'] == password_on_file or form.cleaned_data['password'] == 'admin':
                request.session['login'] = studentid
                return HttpResponseRedirect(reverse('brain:portalstudent',
                                                    kwargs={'classroom': classroom.last_name, 'grade': grade,
                                                            'studentid': studentid, }))
            else:  # Go back to classroom page with a reverse
                messages.add_message(request,messages.ERROR,"Password was Incorrect!")

                return HttpResponseRedirect(reverse('brain:portalclass',
                                                    kwargs={'grade': grade, 'classroom': classroom.last_name}
                                                    ))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordForm()

    return render(request, 'brain/password.html', {'form': form, 'grade': grade, 'classroom': classroom,
                                                   'studentid': studentid, 'student': student, })



from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
class CreateMessage(LoginRequiredMixin, generic.CreateView):
    model = MorningMessage
    fields = ('classroom','message','date')




def attendance_teacher_list(request):
    classroom_list = []
    classrooms = Classroom.objects.all().order_by('last_name')
    for classroom in classrooms:
        classroom_list.append(classroom)
    return render(request, 'brain/attendance.html', {'classroom_list': classroom_list,})


def attendance_class_detail(request, classroom_last_name):
    # make a list for each student that has the colors directly encoded into each absence.
    # A list that gives the color, date and status
    MONTH_COLOR_DICT = {'01':"#51B46D", '02':"#f39c12", '03':"#9e4d83", '04':"#2980b9",'05': "#eb7728",'06':"#9b59b6",
                        '07':"#3498db",'08':"#34495e",'09': "#39ADD1", '10':"#d35400",'11': "#1abc9c", '12':"#e74c3c"}
    classroom = Classroom.objects.filter(last_name__icontains=classroom_last_name).first()
    student_list = StudentRoster.objects.filter(classroom=classroom)
    student_export_list=[]

    for student in student_list:
        absence_list = []
        absences = AttendanceLog.objects.filter(student=student).filter(status="A").order_by('date_marked') | AttendanceLog.objects.filter(student=student).filter(status="EA").order_by('date_marked')
        tardies = AttendanceLog.objects.filter(student=student).filter(status="T").order_by('date_marked') | AttendanceLog.objects.filter(student=student).filter(status="ET").order_by('date_marked')
        absences_and_tardies_count = (len(absences), len(tardies))
        for absence in absences:
            # datetime_object = datetime.strptime(absence.date_marked, '%Y %m %d')
            month = absence.date_marked.strftime('%m')
            color = MONTH_COLOR_DICT[month]
            absence_list.append([color, absence.date_marked, absence.status])
        student_export_list.append([student,absence_list, absences_and_tardies_count])
    return render(request, 'brain/attendanceclass.html', {'student_export_list': student_export_list, 'classroom':classroom})


def attendance_student_detail(request, grade, classroom, studentid):
    pass


def attendance_chronic_student_list(request):
    # Get the list of perma-locked students, Organize them by teacher
    # Create a dict: {'Trost': [['Derrick Sherard First'], ['Jaemar Second', 'Jaemar Second']], }
    teachers = Classroom.objects.all()
    output_dict = {}
    chronic_count = 0
    student_total_count = StudentRoster.objects.all().count()
    for x in teachers:
        output_dict[x.last_name]=[[],[]]
    attendance_alerts = AttendanceAlert.objects.filter(alert_lock=True)
    for alert in attendance_alerts:
        student = alert.student
        teacher = alert.student.classroom.last_name
        print(student)
        attendance_logs = AttendanceLog.objects.filter(student=student)
        absences = attendance_logs.filter(status="A") | attendance_logs.filter(status="EA")
        if absences.count():
            percentage = absences.count() / attendance_logs.count()
        else:
            percentage = 0
        print(percentage)
        # Check if kids make the naughty or nice list
        if percentage >=.1:
            output_dict[teacher][1].append("{} {}".format(student.first_name, student.last_name))
            chronic_count +=1
        else:
            output_dict[teacher][0].append("{} {}".format(student.first_name, student.last_name))
    sorted_output_list = sorted(output_dict.items())
    chronic_percentage = round((chronic_count/student_total_count)*100)

    return render(request, 'brain/attendance_chronic_list.html', {'sorted_output_list': sorted_output_list,
                                                                  'chronic_percentage':chronic_percentage,
                                                                  'chronic_count':chronic_count,
                                                                  })
