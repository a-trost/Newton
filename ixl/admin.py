from django.contrib import admin

# Register your models here.

from .models import IXLSkill, IXLSkillScores, IXLStats, Challenge, ChallengeAssignment, ChallengeExercise, IXLTimeSpent

from .models import IXLList, IXLListAssignment, IXLListChallenge, IXLListChallengeExercise, IXLListExercise, \
    IXLListSkill, IXLListSkillScores


class IXLSkillScoresAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'ixl_skill_id', 'date_recorded', 'score',)
    search_fields = ['student_id__first_name', 'ixl_skill_id__skill_id']


class IXLSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_id', 'skill_description', 'ixl_url', 'category',)
    search_fields = ['skill_description', 'skill_id', 'category']


class IXLStatsAdmin(admin.ModelAdmin):
    list_display = ('student', 'last_practiced', 'questions_answered', 'time_spent')
    list_filter = ('student__current_class__classroom',)


class ChallengeExerciseInline(admin.TabularInline):
    model = ChallengeExercise
    extra = 5


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'challenge_count')
    list_filter = ['date']
    search_fields = ['title']
    inlines = [ChallengeExerciseInline, ]


class ChallengeAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'challenge', 'date_assigned', 'current', 'completed')
    search_fields = ['student_id__first_name', 'student_id__last_name', 'challenge__title', ]
    list_filter = ['date_assigned', 'student_id__current_class__classroom', 'student_id__current_class__grade', ]


class IXLTimeSpentAdmin(admin.ModelAdmin):
    list_display = ['student', 'date_spent', 'aTime', 'bTime', 'cTime', 'dTime', 'eTime', 'fTime', 'gTime', 'hTime',
                    'rewarded_time_total', 'time_goal_met']
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ['student__classroom', 'date_spent',]


class IXLListExerciseInline(admin.TabularInline):
    model = IXLListExercise
    extra = 10


class IXLListAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', ]
    inlines = [IXLListExerciseInline]



admin.site.register(IXLSkillScores, IXLSkillScoresAdmin)
admin.site.register(IXLSkill, IXLSkillAdmin)
admin.site.register(IXLStats, IXLStatsAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeAssignment, ChallengeAssignmentAdmin)
admin.site.register(IXLTimeSpent, IXLTimeSpentAdmin)
admin.site.register(IXLList, IXLListAdmin)
admin.site.register(IXLListChallenge)
admin.site.register(IXLListAssignment, )
admin.site.register(IXLListChallengeExercise, )
admin.site.register(IXLListExercise, )
admin.site.register(IXLListSkill, )
admin.site.register(IXLListSkillScores, )
