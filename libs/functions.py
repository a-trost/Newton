from collections import Counter

from nwea.models import NWEASkill, NWEAScore, RITBand
from brain.models import StudentRoster, Classroom, CurrentClass, AccountInfo, MorningMessage, MorningMessageSettings, \
    Schedule, TeacherSettings
from ixl.models import IXLSkillScores, ChallengeAssignment, ChallengeExercise, IXLSkill, Challenge
from variables import cbaExercises
import brain.templatetags.brain_extras
# from variables import *
import requests
import datetime
import inspect


# Find highest NWEA subdomain level that you know a student has passed (either from NWEA results or IXL),
# Have NWEA RIT Level scores for each student
# Can compute if they've passed a RIT Band from IXL
# Start with NWEA Rit band as a floor in each subdomain
# Then check IXL for the next level - have they passed? If so go to next level
#
# In the classroom report - what NWEA subdomain level they're working, and do you think they've passed the previous level because of NWEA test (w/date) or IXL.
#
# Result of this calculation =
# Student -> Set of NWEA RIT bands they should be working on (in each subdomain)
# Sort by RIT band number, return top 10
#
# Add another column for CBA with the mapping of NWEA and IXL. If the CBA column is yes (or an upcoming date) Move to top of list of ten.
#
#
# Add fields to IXL Test objects -> CBA Spring | CBA Fall
# CBA Test objects, IXL Tests can map to a CBA test

#
# Classroom page - X kids need skill Y
# Work off of full set of IXL skills for each kid, not the top 10
# Iterate all kids, their sets, count up the # that need each skill, take the top X skills with more than Y kids
# Max 1+ per subdomain?
# Bubble up CBA things here too?
# Print out everything, group by subdomain



# Desired Outputs:
# List of IXL tests for each student (+more detail on classroom page)
# List of IXL tests that many students need + lists of those students for each test (some # of these)
# Secondary:
# Test-centric view (Text X is coming up, what do students need to work on for it)


# TODO: Sort list by most occurring skills, trim at top 10 items.
# TODO: include specific students in the list, so you know who to teach.

def class_skills_list(student_list, arg):
    class_skill_list = []
    for student in student_list:
        single_skill_list = nwea_recommended_skills_list(student, "recommended_skill_list")
        for item in single_skill_list:
            class_skill_list.append(item)
    count = Counter(class_skill_list)
    class_skill_list = count.most_common()
    return class_skill_list


def nwea_recommended_skills_list(student, arg):
    '''Gets back list of next skills for student. value is a student object
    '''
    try:
        # student = StudentRoster.objects.get() # Temporary example for development.
        if NWEAScore.objects.filter(student=student).count() > 0:  # If student has NWEA Test Scores
            recent_nwea_scores = NWEAScore.objects.all().get(
                student=student)  # .order_by(NWEAScore.test_period).first()
            sub1 = recent_nwea_scores.subdomain1
            sub2 = recent_nwea_scores.subdomain2
            sub3 = recent_nwea_scores.subdomain3
            sub4 = recent_nwea_scores.subdomain4
            sub5 = recent_nwea_scores.subdomain5
            sub6 = recent_nwea_scores.subdomain6
            sub7 = recent_nwea_scores.subdomain7
            sub8 = recent_nwea_scores.subdomain8
            subdomain_scores = [sub1, sub2, sub3, sub4, sub5, sub6, sub7, sub8]

        else:  # Otherwise, assume student is at RIT 141 and build from there with IXL.
            subdomain_scores = [161, 161, 161, 161, 161, 161, 161, 161]
    except:
        raise IndexError

    # TODO: If student has CBA + ENI Scores get those too.
    # Else:
    # 	Assume they know nothing.


    # Get skills that match their RIT bands
    recommended_skill_list = []  # Create blank list of recommended skills for this student
    estimated_nwea_scores = []
    subdomain_percentage_complete = []
    for x in range(0, 8):  # Iterate through the 8 subdomains, 1 at a time.
        loop = True
        additional_rit_score = 0
        while loop:
            count_of_passed_skills_in_band = 0  # Reset passed Skill counter
            current_rit_band = subdomain_scores[x] + additional_rit_score
            skills_from_current_rit_band = NWEASkill.objects.filter(rit_band__subdomain=(x + 1),
                                                                    rit_band__rit_band=current_rit_band)
            number_of_skills_from_current_rit_band = skills_from_current_rit_band.count()
            for skill in skills_from_current_rit_band:
                if skill.ixl_match:  # if skill has the field ixl_match filled out, then look and see if that match has been passed
                    try:  # Try to get the student's score for this IXL Skill
                        ixl_pass = IXLSkillScores.objects.get(
                            ixl_skill_id__skill_id=skill.ixl_match, student_id__student_id=student.student_id)
                        ixl_score = ixl_pass.score
                    except:  # Else, assume score is 0
                        ixl_score = 0
                    if ixl_score >= 80:
                        count_of_passed_skills_in_band += 1
                    else:
                        dupe = False
                        if len(recommended_skill_list) > 0:  # Check if the list has anything at all
                            for j in recommended_skill_list:  # Pull out a tuple of 3 things
                                for i in j:
                                    if skill.ixl_match == i:
                                        dupe = True
                        if dupe == False:
                            subdomain = x
                            recommended_skill_list.append((skill.ixl_match, skill.skill, current_rit_band, subdomain))
            insufficient_skills_passed = count_of_passed_skills_in_band < number_of_skills_from_current_rit_band
            if number_of_skills_from_current_rit_band == 0 or insufficient_skills_passed:
                break
            elif count_of_passed_skills_in_band == number_of_skills_from_current_rit_band:
                additional_rit_score += 10
                continue
        estimated_nwea_scores.append(current_rit_band)
        try:  # Catches if there are no NWEA Skills in the DB.
            complete_percentage = percentage(count_of_passed_skills_in_band, number_of_skills_from_current_rit_band)
        except ZeroDivisionError:
            complete_percentage = 0
        subdomain_percentage_complete.append(str(complete_percentage))
    recommended_skill_list.sort(key=lambda tup: tup[2])
    actual_nwea_scores = subdomain_scores

    if arg == "actual_nwea_scores":
        return actual_nwea_scores
    elif arg == "estimated_nwea_scores":
        return estimated_nwea_scores
    elif arg == "recommended_skill_list" or arg == "":
        return recommended_skill_list
    elif arg == "subdomain_percentage_complete":
        return subdomain_percentage_complete
    elif arg == 'all':
        return actual_nwea_scores, estimated_nwea_scores, recommended_skill_list, subdomain_percentage_complete
    else:
        return None


def percentage(part, whole):
    answer = 100 * float(part) / float(whole)
    answer = int(round(answer))
    return answer


##  PARENT LETTER FUNCTIONS ==========================================================================================

def get_current_ixl_challenge(student):
    try:
        ixl_challenge_assignment = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
    except:
        ixl_challenge_assignment = False

    if ixl_challenge_assignment:  # get challenge
        challenge_exercise_list = []  # [(id, description, score), ]
        bonus_exercise_list = []
        current_ixl_challenge = ixl_challenge_assignment.challenge
        exercise_list = ChallengeExercise.objects.filter(challenge=current_ixl_challenge)  # Get the related exercises
        for exercise in exercise_list:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student,
                                                            ixl_skill_id__skill_id=exercise.exercise_id).score
            except:
                exercise_score = 0
            required_score = exercise.required_score
            if exercise.bonus == True:
                bonus_exercise_list.append((exercise.exercise_id, required_score, exercise_score))
            else:
                challenge_exercise_list.append((exercise.exercise_id, required_score, exercise_score))
            # Get scores for each challenge
    else:
        challenge_exercise_list = None
        current_ixl_challenge = None
        bonus_exercise_list = None
    return challenge_exercise_list, bonus_exercise_list


def get_current_amc_challenge(student):
    current_test = brain_extras.amc_number_to_text(brain_extras.current_amc_test(student))
    current_test_name = current_test.name  # Statue of Liberty
    current_test_signifier = current_test.topic  # Keeps a string for "Addition 1" or "Subtraction 5" or "Fractions"
    current_test_topic = current_test.topic.replace(" ",
                                                    "").upper()  # Get the Topic (Addition 3) and turn it into ADDITION3
    if 'SUBTRACTION' in current_test_topic:  # This is for the Template so it knows if we're adding or subtracting
        test_type = 'SUB'
    elif "ADDITION" in current_test_topic:
        test_type = 'ADD'
    elif "MULTIPLICATION" in current_test_topic:
        test_type = 'MUL'
    else:
        test_type = "IMAGE"  # This will be used for clocks, coins, etc.
    combination_set = TESTDICTIONARY[current_test_topic]
    return combination_set, test_type, current_test_name


def parent_letter(student):
    pass


from django.core.mail import EmailMessage


def send_an_email():
    email = EmailMessage(
        subject='Hello',
        body='''Body goes here.
             How are you?
             I hope this email works!''',
        from_email='newton@newtonthinks.com',
        to=['ins-dauaprqb@isnotspam.com'],
        reply_to=['alextrostbtwa@gmail.com.com'],
        headers={'Content-Type': 'text/plain'},
    )
    email.send()


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox791822b6aeca4aee8007134fecd331ec.mailgun.org/messages",
        auth=("api", mailgun_apikey),
        data={"from": "Mailgun Sandbox <postmaster@sandbox791822b6aeca4aee8007134fecd331ec.mailgun.org>",
              "to": "Alex <alexrtrost@gmail.com>",
              "subject": "Test 2 Alex",
              "text": "Congratulations Alex, you just sent an email with Mailgun!  You are truly awesome!"})


def get_nearest_monday(date_arg=False):
    """
    If today is Mon-Friday, return that Monday. If Sat-Sun, move forward and return upcoming Monday.
    Used to return a consistent 'start of week' for various modules.
    :return: datetime object
    """
    DAY_DICT = {0: 1, 1: 0, 2: -1, 3: -2, 4: -3, 5: -4, 6: 2, }
    if date_arg:
        todays_date = date_arg
    else:
        todays_date = datetime.date.today()
    days_away = datetime.timedelta(days=DAY_DICT[int(todays_date.strftime('%w'))])
    return (todays_date + days_away)


##  IXL CHALLENGE FUNCTIONS ==========================================================================================

def get_student_list(classroom=None, grade=None, student=None):
    """
    :param classroom: Takes a classroom object or a classroom's last name
    :param grade: takes a grade title ("2nd")
    :param student: takes a student object or a student's full name
    :return: A list of StudentRoster objects
    """
    if classroom:
        if inspect.isclass(classroom):
            return StudentRoster.objects.filter(current_class__classroom=classroom)
        else:
            try:
                return StudentRoster.objects.filter(current_class__classroom__last_name=classroom)
            except:
                print('Classroom {} could not be found.'.format(classroom))
    elif grade:
        try:
            return StudentRoster.objects.filter(current_class__grade__contains=grade)
        except:
            print('Grade {} could not be found.'.format(classroom))
    elif student:
        if inspect.isclass(student):
            return student
        else:
            try:
                return StudentRoster.objects.filter(last_name__in=student).filter(first_name__in=student)
            except:
                print('Student {} could not be found.'.format(classroom))


def make_mastery_challenge(student, current_challenge):
    """
    Creates one challenge that the student must get 100 on to count as "complete"
    :param student:
    :param current_challenge:
    :return:
    """
    for item in mastery_skills:
        skill_score = IXLSkillScores.objects.filter(student_id=student, ixl_skill_id__skill_id=item)
        if skill_score.exists():
            if skill_score.score < 96:
                challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                      exercise_id=item,
                                                                      required_score=100, )
                return
        else:
            challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                  exercise_id=item,
                                                                  required_score=100)
        return

    return


def make_cba_challenge(student, current_challenge, bonus_exercise=False):
    """
    Creates one challenge that is aligned to the upcoming CBA.
    :param student:
    :param current_challenge:
    :return:
    """
    for item in cbaExercises:
        if not ChallengeExercise.objects.filter(challenge=current_challenge,exercise_id=item,).exists():
            skill_score = IXLSkillScores.objects.filter(student_id=student, ixl_skill_id__skill_id=item).first()
            # print(skill_score)
            try:
                if skill_score.score:
                    if skill_score.score < 78:
                        # print("Assigning {} Tripped 1".format(skill_score))
                        obj, created = ChallengeExercise.objects.get_or_create(challenge=current_challenge,
                                                                              exercise_id=item,
                                                                              required_score=80,
                                                                               bonus=bonus_exercise)
                        if created: return


                else:
                    # print("Tripped 2")
                    obj, created = ChallengeExercise.objects.get_or_create(challenge=current_challenge,
                                                                          exercise_id=item,
                                                                          required_score=80,
                                                                           bonus=bonus_exercise)
                    if created: return
            except:
                # print("Tripped 3")
                obj, created = ChallengeExercise.objects.get_or_create(challenge=current_challenge,
                                                                       exercise_id=item,
                                                                       required_score=80,
                                                                       bonus=bonus_exercise)
                if created: return

    print("Ran out of cba exercises for {}!".format(student))
    return


def make_nwea_challenge(student, current_challenge, bonus_exercise=False):
    """
    Creates one challenge that is aligned to the student's NWEA scores.
    :param student:
    :param current_challenge:
    :return:
    """
    skill_list = nwea_recommended_skills_list(student, "recommended_skill_list")
    domain_list = []
    waiting_list = []
    for skill in skill_list:
        print("Exercise {} - beginning".format(skill[0]))
        # First check if skill has been assigned to student before. if more than 3 times, skip skill.
        previously_assigned = ChallengeExercise.objects.filter(challenge__challengeassignment__student_id=student,
                                                               exercise_id=skill[0], )
        previously_assigned_count = len(previously_assigned)
        if previously_assigned_count > 3:
            continue
        if skill[3] in domain_list:  # Domain_list is for the 8 domains of the NWEA
            waiting_list.append(skill[
                                    0])  # Waiting list is for if we need to add 2 NWEA skills from the same domain due to not having enough exercises
        else:
            domain_list.append(skill[3])  # Add this domain to the list
            # Create a Challenge Exercise object with the challenge and skill
            print("Exercise {} - Else 3".format(skill[0]))
            try:
                ChallengeExercise.objects.create(challenge=current_challenge, exercise_id=skill[0],
                                                 bonus=bonus_exercise)
                return
            except AttributeError:
                print("Exercise {}".format(skill[0]))
                continue
            except:
                continue
    for skill in waiting_list:
        try:
            print("Exercise {} - Waiting List".format(skill))
            challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge, bonus=bonus_exercise,
                                                                  exercise_id=skill)
            return
        except:
            continue

def create_ixl_challenge(student):
    try:
        classroom_settings = TeacherSettings.objects.get(classroom=student.current_class.classroom)
        mastery_num, cba_num, nwea_num, bonus_num = classroom_settings.mastery_exercises, classroom_settings.cba_exercises, \
                                                    classroom_settings.nwea_exercises, classroom_settings.bonus_exercises
    except:
        mastery_num, cba_num, nwea_num, bonus_num = 1, 2, 2, 5
    nearest_monday_date_obj = get_nearest_monday()
    nearest_monday = nearest_monday_date_obj.strftime('%-m/%-d')
    title = "{} {}'s {} Challenge".format(student.first_name, student.last_name[0], nearest_monday)
    if Challenge.objects.filter(title=title, date=nearest_monday_date_obj).exists():
        Challenge.objects.filter(title=title, date=nearest_monday_date_obj).delete()
    current_challenge = Challenge.objects.create(title=title, date=nearest_monday_date_obj)

    for _ in range(3):
        make_cba_challenge(student, current_challenge)
    for _ in range(13):
        make_cba_challenge(student, current_challenge, bonus_exercise=True)

    # for _ in range(mastery_num):
    #     make_mastery_challenge(student, current_challenge)
    # for _ in range(cba_num):
    #     make_cba_challenge(student, current_challenge)
    # for _ in range(nwea_num):
    #     make_nwea_challenge(student, current_challenge)
    # for _ in range(bonus_num):  # Make bonus exercises
    #     make_nwea_challenge(student, current_challenge, bonus_exercise=True)
    print("Assigning {} to {}".format(title, student))
    obj, created = ChallengeAssignment.objects.get_or_create(student_id=student, challenge=current_challenge, )
    return obj, created
