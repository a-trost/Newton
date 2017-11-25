import datetime

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from brain.models import StudentRoster
from variables import GRADE_CHOICES
from django.utils.timezone import now



class IXLSkill(models.Model):
    ixl_format = RegexValidator(r'^\w+\-\w+\.\d+$', 'Pattern must match IXL format: D-A.12')
    skill_id = models.CharField(max_length=7, validators=[ixl_format], blank=False, verbose_name='Skill ID')
    skill_description = models.CharField(max_length=200, blank=True, verbose_name='Skill Description')
    ixl_url = models.CharField(max_length=300, blank=True, verbose_name='IXL URL', default="")
    category = models.CharField(max_length=100, null=True)

    def __str__(self):
        return '%s - %s - %s' % (self.category, self.skill_id, self.skill_description)

    class Meta:
        verbose_name = 'IXL Skill'
        verbose_name_plural = 'IXL Skills'
        ordering = ['skill_id']


class IXLSkillScores(models.Model):  # Intersection of IXLSkill and Student Roster
    student_id = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, )
    ixl_skill_id = models.ForeignKey(IXLSkill, on_delete=models.CASCADE, verbose_name='IXL Skill ID', )
    date_recorded = models.DateField(default=datetime.date.today, verbose_name='Date Recorded')
    score = models.IntegerField()

    def passing_score(self):
        if self.score >= 80:
            return True
        elif self.score < 80:
            return False
        else:
            raise ValueError

    def __str__(self):
        return '%s - %s - %s' % (self.student_id, self.ixl_skill_id, self.score)

    class Meta:
        verbose_name = 'IXL Score'
        verbose_name_plural = 'IXL Scores'
        unique_together = ("student_id", "ixl_skill_id")
        ordering = ['student_id', 'ixl_skill_id']


class Challenge(models.Model):  # The saved recommendation sheet to check for completion
    title = models.CharField(max_length=250, default="Challenge", verbose_name="Challenge Title", unique=True)
    date = models.DateField(default=datetime.date.today, verbose_name='Date Created')

    def __str__(self):
        return '%s' % (self.title,)

    class Meta:
        verbose_name = 'IXL Challenge'
        verbose_name_plural = 'IXL Challenges'
        ordering = ['-date', 'title']

    def challenge_count(self):
        return len(ChallengeExercise.objects.filter(challenge=self, bonus=False))


class ChallengeExercise(models.Model):
    challenge = models.ForeignKey(Challenge)
    exercise_id = models.CharField(max_length=10)
    required_score = models.IntegerField(default=80, blank=False, null=False)
    bonus = models.BooleanField(default=False, )

    def __str__(self):
        return '%s - %s' % (self.challenge, self.exercise_id)

    class Meta:
        unique_together = (("challenge", "exercise_id"),)


class ChallengeAssignment(models.Model):  # Assigns a challenge to a specific student(s)
    student_id = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, )
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_assigned = models.DateField(default=datetime.date.today, verbose_name='Date Assigned')

    # current_challenge = models.BooleanField(default=True)
    # complete = models.BooleanField(default=False)


    def current(self):
        assignment = ChallengeAssignment.objects.filter(student_id=self.student_id).latest('date_assigned')
        if assignment.pk == self.pk:
            return True
        else:
            return False

    current.boolean = True

    def last_turned_in(self):
        assignment = ChallengeAssignment.filterByQuery(name='student_id', arg=self.student_id).latest('date_turned_in')
        if assignment.pk == self.pk:
            return True
        else:
            return False

    current.boolean = True

    def completed(self):
        exercises = ChallengeExercise.objects.filter(challenge=self.challenge, bonus=False)
        total_complete, total_questions = 0, 0
        for exercise in exercises:
            try:
                total_questions += 1
                ixl_skill_id = IXLSkill.objects.get(skill_id=exercise.exercise_id)
                score = IXLSkillScores.objects.get(student_id=self.student_id, ixl_skill_id=ixl_skill_id)
                required_score = exercise.required_score

                if score.score >= required_score:
                    total_complete += 1
                else:
                    pass
            except:
                pass

        return total_complete, total_questions

    def __str__(self):
        return '%s : %s' % (self.challenge, self.student_id)

    class Meta:
        verbose_name = 'IXL Challenge Assignment'
        verbose_name_plural = 'IXL Challenge Assignments'
        ordering = ['-date_assigned', 'challenge', 'student_id']


class IXLStats(models.Model):
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, )
    ixl_user_id = models.IntegerField(blank=True, verbose_name="IXL UserID#", default=0, null=True)
    last_practiced = models.IntegerField(verbose_name="Last Practiced", blank=True, default=20)
    questions_answered = models.IntegerField(verbose_name="Questions Answered", blank=True, default=0)
    time_spent = models.IntegerField(verbose_name="Time Spent", blank=True, default=0)

    class Meta:
        verbose_name = 'IXL Stat'
        verbose_name_plural = 'IXL Stats'
        # unique_together = ("student", "ixl_skill_id")


class IXLTimeSpent(models.Model):
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, )
    date_spent = models.DateField(default=datetime.date.today, verbose_name='Date Practiced')
    aTime = models.IntegerField(verbose_name="Pre-K Seconds Spent", default=0)
    bTime = models.IntegerField(verbose_name="Kinder. Seconds Spent", default=0)
    cTime = models.IntegerField(verbose_name="1st Grade Seconds Spent", default=0)
    dTime = models.IntegerField(verbose_name="2nd Grade Seconds Spent", default=0)
    eTime = models.IntegerField(verbose_name="3rd Grade Seconds Spent", default=0)
    fTime = models.IntegerField(verbose_name="4th Grade Seconds Spent", default=0)
    gTime = models.IntegerField(verbose_name="5th Grade Seconds Spent", default=0)
    hTime = models.IntegerField(verbose_name="6th Grade Seconds Spent", default=0)

    # Some way to look up the grades on either side of the student's current grade so that
    # we can give credit only for doing tasks at those levels. Not rewarding 4th graders for 1st grade work.

    class Meta:
        verbose_name = 'IXL Time Spent'
        verbose_name_plural = 'IXL Time Spent'
        unique_together = ("student", "date_spent")

    def entire_time_total(self):
        return self.aTime + self.bTime + self.cTime + self.dTime + self.eTime + self.fTime + self.gTime + self.hTime

    def rewarded_time_total(self):
        grade_dict = {'K': 0, '1st': 1, '2nd': 2, '3rd': 3, '4th': 4, '5th': 5, '6th': 6, '7th': 7, }
        time_grade_dict = {-1: self.aTime, 0: self.bTime, 1: self.cTime, 2: self.dTime, 3: self.eTime, 4: self.fTime,
                           5: self.gTime, 6: self.hTime}
        try:
            current_grade = self.student.classroom.grade
            # get the number for the grade
            grade_number = grade_dict[current_grade]
            # get the time for the current grade, the grade +1 and the grade -1
            return time_grade_dict[grade_number]  # + time_grade_dict[grade_number - 1] + time_grade_dict[
            # grade_number + 1]
        except:
            return None

    def time_goal_met(self):
        if self.rewarded_time_total() >=600:
            return True
        else:
            return False


    def __str__(self):

        return "{}, {}, {} seconds".format(self.student, self.date_spent, self.rewarded_time_total())

############## NEW IXL MODELS #####################

class IXLListSkill(models.Model):
    ixl_format = RegexValidator(r'^\w+\.\d+$', 'Pattern must match IXL format: A.12')
    grade = models.CharField(max_length=1)
    id_code = models.CharField(max_length=6, validators=[ixl_format], blank=False, verbose_name='Skill ID')
    description = models.CharField(max_length=200, blank=True, verbose_name='Skill Description')
    category = models.CharField(max_length=100, null=True)

    def __str__(self):
        return '%s - %s - %s - %s' % (self.grade, self.category, self.id_code, self.description)

    class Meta:
        verbose_name = 'IXL List Skill'
        verbose_name_plural = 'IXL List Skills'
        ordering = ['id_code']


class IXLListSkillScores(models.Model):  # Intersection of IXLSkill and Student Roster
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, )
    skill = models.ForeignKey(IXLListSkill, on_delete=models.CASCADE, verbose_name='IXL List Skill', )
    date_recorded = models.DateField(default=datetime.date.today, verbose_name='Date Recorded')
    score = models.IntegerField()

    def passing_score(self):
        if self.score >= 80:
            return True
        elif self.score < 80:
            return False
        else:
            raise ValueError

    def __str__(self):
        return '%s - %s - %s' % (self.student, self.skill, self.score)

    class Meta:
        verbose_name = 'IXL Score'
        verbose_name_plural = 'IXL Scores'
        unique_together = ("student", "skill")
        ordering = ['student_id', 'skill']


CATEGORY_CHOICES = (
("Unit", "Unit"), ("Remediation", "Remediation"), ("Enrichment", "Enrichment"), ("Test", "Test"), ("Other", "Other"))


class IXLList(models.Model):
    '''List for IXL Exercises that can be assigned to specific students'''
    title = models.CharField(max_length=255, )
    author = models.ForeignKey(User)
    description = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=65)

    class Meta:
        verbose_name = 'IXL List'
        verbose_name_plural = 'IXL Lists'
        unique_together = (('title', 'author'),)

    def __str__(self):
        return self.title

class IXLListAssignment(models.Model):
    '''Assigns the List to specific students'''
    student = models.ForeignKey(StudentRoster)
    ixl_list = models.ForeignKey(IXLList)
    assigned = models.BooleanField(default=True)
    date_created = models.DateField(default=now)
    number_to_assign = models.IntegerField()

    class Meta:
        verbose_name = 'IXL List Assignment'
        verbose_name_plural = 'IXL List Assignments'

    def progress(self):
        '''returns exercises_completed, exercises_total'''
        exercises = self.ixl_list.ixllistexercise_set
        exercises_completed = 0
        for exercise in exercises:
            exercise_log = IXLListSkillScores.objects.filter(student=self.student, skill=exercise).first()
            if exercise_log:
                if exercise_log.score >= exercise.required_score:
                    exercises_completed += 1

class IXLListExercise(models.Model):
    '''The specific Exercises that the IXLlist contains.'''
    list = models.ForeignKey(IXLList)
    list_skill = models.ForeignKey(IXLListSkill, null=True)
    required_score = models.IntegerField(default=80, blank=False, null=False)
    order = models.IntegerField(default=1,)

    def __str__(self):
        return '%s - %s' % (self.list, self.list_skill)

    class Meta:
        unique_together = (("list", "list_skill", "required_score"),)
        verbose_name = 'IXL List Exercise'
        verbose_name_plural = 'IXL List Exercises'

class IXLListChallenge(models.Model):
    '''Challenges Unique to each student that is assembled from several lists.'''
    date = models.DateField(default=datetime.date.today, verbose_name='Date Created')
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, )
    active = models.BooleanField(default=True)
    achieved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'IXL List Challenge'
        verbose_name_plural = 'IXL List Challenges'

    def progress(self):
        '''Returns # total challenges and # challenges completed'''
        challenges_completed = 0
        for exercise in self.ixllistchallengeexercise_set:
            if exercise.completed():
                challenges_completed += 1
        return self.ixllistchallengeexercise_set.filter(bonus=False).count(), challenges_completed

    def check_if_achieved(self):
        if self.active:
            total_challenges, challenges_completed = self.progress()
            if total_challenges == challenges_completed and total_challenges > 0:
                self.achieved = True

    def check_if_active(self):
        latest_challenge = IXLListChallenge.objects.filter(student=self.student).latest('date')
        if latest_challenge.date != self.date:
            self.active = False

class IXLListChallengeExercise(models.Model):
    '''The exercises that are assigned to a challenge and must be completed by a student'''
    challenge = models.ForeignKey(IXLListChallenge)
    list_exercise = models.ForeignKey(IXLListExercise, null=True)
    required_score = models.IntegerField(default=80, blank=False, null=False)
    bonus = models.BooleanField(default=False, )

    def __str__(self):
        return '%s - %s' % (self.challenge, self.list_exercise)

    class Meta:
        verbose_name = 'IXL List Challenge Exercise'
        verbose_name_plural = 'IXL List Challenges Exercises'
        unique_together = (("challenge", "list_exercise"),)

    def completed(self):
        student, required_score = self.challenge.student, self.list_exercise.required_score
        current_score = IXLListSkillScores.objects.filter(student=student, skill=self.list_exercise.list_skill)
        return current_score >= required_score
