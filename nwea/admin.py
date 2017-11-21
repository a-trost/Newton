from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea


# Register your models here.

from .models import RITBand, NWEAScore, NWEASkill, NWEAAverage, NWEAGoal


class NWEASkillAdmin(admin.ModelAdmin):
    list_display = ('rit_band', 'skill', 'ixl_match',)
    list_filter = ['rit_band__domain','rit_band__subdomain', 'rit_band__rit_band']
    search_fields = ['ixl_match']
    list_editable = ['ixl_match']

class NWEAScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'season', 'subdomain1', 'subdomain2', 'subdomain3', 'subdomain4',
                    'subdomain5', 'subdomain6', 'subdomain7', 'subdomain8')
    list_editable = ('subdomain1',  'season', 'subdomain2', 'subdomain3', 'subdomain4',
                    'subdomain5', 'subdomain6', 'subdomain7', 'subdomain8')

class NWEAGoalAdmin(admin.ModelAdmin):
    list_display = ('student', 'math_winter', 'reading_winter', 'math_spring', 'reading_spring')
    list_editable = ('math_winter', 'reading_winter', 'math_spring', 'reading_spring')
    search_fields = ['student__first_name','student__last_name']

class NWEAAverageAdmin(admin.ModelAdmin):
    list_display = ('student', 'math_fall','reading_fall', 'math_winter', 'reading_winter','math_spring','reading_spring')
    list_editable = ['math_fall', 'reading_fall', 'math_winter', 'reading_winter', 'math_spring', 'reading_spring']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '8'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '8'})},
    }



admin.site.register(RITBand)
admin.site.register(NWEASkill, NWEASkillAdmin)
admin.site.register(NWEAScore, NWEAScoreAdmin)
admin.site.register(NWEAGoal, NWEAGoalAdmin)
admin.site.register(NWEAAverage, NWEAAverageAdmin)
