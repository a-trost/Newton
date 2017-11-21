from django.contrib import admin
from django.contrib.admin import AdminSite
from django.forms import TextInput, Textarea
from django.db import models

from .models import Classroom, CurrentClass, StudentRoster, AccountInfo, \
    ReadingStats, MorningMessage, MorningMessageSettings, Subject, Schedule, DataUpdate, SchoolDay, SubjectUnit, \
    WeeklyWord, BehaviorReport, CommonCoreStateStandard, HomeworkCompletion, TeacherSettings, ClassroomAssignment, \
    ClassroomAccountPassword, ReadingTimeSpent, StreakHighScore, AttendanceLog, AttendanceAlert, StudentUserAccount

'''
class BrainAdminSite(AdminSite):
    site_header = 'Newton Administration'
'''
admin.site.site_title = 'Newton Admin Page'
admin.site.site_header = 'Newton Admin Page'


class AttendanceLogAdmin(admin.ModelAdmin):
    search_fields = ['student__first_name', 'student__last_name', 'status']
    list_display = ['student', 'date_marked', 'status']
    list_filter = ['status', 'date_marked', 'student__classroom']

class AttendanceAlertAdmin(admin.ModelAdmin):
    search_fields = ['student__first_name', 'student__last_name', ]
    list_display = ['student', 'alert_lock']
    list_editable = ['alert_lock',]
    list_filter = ['student__classroom',]

class DataUpdateAdmin(admin.ModelAdmin):
    list_display = ('dateandtime',)

class StudentInline(admin.TabularInline):
    model = StudentRoster
    extra = 3

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name', 'grade', 'email', 'remindURL', 'workphone')
    list_editable = ('email', 'remindURL', 'workphone')
    inlines = [StudentInline]

class ClassroomAccountPasswordAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'site', 'username',)
    fieldsets = [
        ('Class and Website', {'fields': ['classroom', 'site']}),
        ('Username and Password', {'fields': ['username', 'password' ]}),
    ]

class StudentRosterAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name and Class', {'fields': ['first_name', 'last_name', 'current_class', 'classroom']}),
        ('Extra Details', {'fields': ['date_of_birth', 'gender', 'email', 'email2']}),
        ('Quickschools', {'fields': ['quickschools_id', ]}),
    ]
    list_display = ('first_name', 'last_name', 'current_class', 'classroom', 'gender', 'date_of_birth','quickschools_id',)
    list_filter = ['classroom', 'classroom__grade']
    radio_fields = {'gender': admin.HORIZONTAL}
    search_fields = ['first_name', 'last_name', 'current_class__classroom__last_name', ]
    list_editable = ['current_class','quickschools_id',]


class CurrentClassAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'grade',)
    list_filter = ['grade',]
    inlines = [StudentInline]


class AccountInfoAdmin(admin.ModelAdmin):
    list_display = ('student', 'ixluser', 'ixlpass', 'kidsazteacher', 'kidsazuser', 'kidsazpass',
                    'myonuser', 'myonpass', 'readworkscode')
    list_filter = ('student__current_class__classroom', 'student__current_class__grade',)
    list_editable = ['kidsazuser', 'kidsazteacher', 'ixlpass', 'kidsazpass', 'myonpass', 'myonuser', 'readworkscode']
    search_fields = ['ixluser', 'myonuser', 'kidsazteacher', 'student__first_name', 'student__last_name']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '10'})},
    }


class ReadingStatsAdmin(admin.ModelAdmin):
    list_display = (
    'student', 'starting_lexile', 'current_lexile', 'goal_lexile', 'lexile_progress', 'myon_tests_taken',
    'myon_time_spent', 'myon_tests_taken', 'myon_books_finished',
    'myon_books_opened')
    list_editable = ['goal_lexile',]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '4'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '4'})},
    }
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ['student__current_class__classroom']


class SpecialScheduleAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    list_editable = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


class MorningMessageAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'date', 'message']
    list_editable = ['date', 'message']
    list_filter = ['classroom']


# class MorningMessageSettingsAdmin(admin.ModelAdmin):
#     list_display = ['classroom', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
#     list_editable = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
    'classroom', 'day', 'subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6', 'subject7',)
    list_editable = ('day', 'subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6', 'subject7',)
    list_filter = ('classroom', 'day',)


class SchoolDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'halfday', 'noschool')
    list_editable = ('halfday', 'noschool')
    list_filter = ('day', 'halfday', 'noschool')


class SubjectUnitAdmin(admin.ModelAdmin):
    list_display = ['grade', 'subject', 'number', 'title', 'datestarted', ]


class WeeklyWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'date_taught', 'keytosuccess', 'quadrant']


class BehaviorReportAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_day', 'data']
    list_filter = ['data','student__current_class', 'student__current_class__grade',]
    list_editable = ['data', ]


class CommonCoreStateStandardAdmin(admin.ModelAdmin):
    list_display = ('grade', 'domain', 'subdomain', 'topic', 'code', 'description')
    list_filter = ('domain', 'subdomain',)
    search_fields = ['grade', 'domain', 'subdomain', 'topic', 'code', 'description']


class HomeworkCompletionAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_day', 'status']
    list_filter = ['status','student__current_class', 'student__current_class__grade',]
    list_editable = ['status', ]
    search_fields = ['student__first_name', 'student__last_name']


# class SchoolAdmin(admin.ModelAdmin):
#     list_display = ['name', 'state', 'zip', 'grade_pre', 'grade_ele', 'grade_mid','grade_hig']
#     list_filter = [ 'name']
#

class TeacherSettingsAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'ixl_level_display']
    list_editable = ['ixl_level_display',]

class ClassroomAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'classroom']

class ReadingTimeSpentAdmin(admin.ModelAdmin):
    list_display = ["student", "date_spent", "time_spent"]
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ['student__classroom', 'date_spent',]

class StreakHighScoreAdmin(admin.ModelAdmin):
    list_display = ["student", "site", "days_in_a_row", "date_achieved"]
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ['student__classroom',]

class StudentUserAccountAdmin(admin.ModelAdmin):
    list_display = ['student', 'user']
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ['student__classroom',]


admin.site.register(StudentRoster, StudentRosterAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(CurrentClass, CurrentClassAdmin)
admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(ReadingStats, ReadingStatsAdmin)
admin.site.register(MorningMessage, MorningMessageAdmin)
admin.site.register(MorningMessageSettings,)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(DataUpdate, DataUpdateAdmin)
admin.site.register(SchoolDay, SchoolDayAdmin)
admin.site.register(SubjectUnit, SubjectUnitAdmin)
admin.site.register(WeeklyWord, WeeklyWordAdmin)
admin.site.register(BehaviorReport, BehaviorReportAdmin)
admin.site.register(CommonCoreStateStandard, CommonCoreStateStandardAdmin)
admin.site.register(HomeworkCompletion, HomeworkCompletionAdmin)
admin.site.register(TeacherSettings, TeacherSettingsAdmin)
admin.site.register(ClassroomAssignment, ClassroomAssignmentAdmin)
admin.site.register(ClassroomAccountPassword, ClassroomAccountPasswordAdmin)
admin.site.register(ReadingTimeSpent, ReadingTimeSpentAdmin)
admin.site.register(StreakHighScore, StreakHighScoreAdmin)
admin.site.register(AttendanceLog, AttendanceLogAdmin)
admin.site.register(AttendanceAlert, AttendanceAlertAdmin)
admin.site.register(StudentUserAccount, StudentUserAccountAdmin)