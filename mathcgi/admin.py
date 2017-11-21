from django.contrib import admin
from django import forms
from .models import CGI, CGIResult
# Register your models here.

def set_zero(modeladmin, request, queryset):
    queryset.update(progress='0')

set_zero.short_description = "Set selected results to 0"

def set_untested(modeladmin, request, queryset):
    queryset.update(progress='-')

set_untested.short_description = "Reset results to Untested"

def set_mastered(modeladmin, request, queryset):
    queryset.update(progress='3')

set_mastered.short_description = "Set selected results to Mastered"

def add_one(modeladmin, request, queryset):
    for query in queryset:
        if query.progress == '0':
            query.progress ='1'
        elif query.progress == '1':
            query.progress ='2'
        elif query.progress=='2':
            query.progress='3'
        elif query.progress=='-':
            query.progress ='3'
        elif query.progress == '3':
            pass
        query.save()


add_one.short_description = "Set selected to increase by 1. Untested will turn to Mastered"


class CGIAdmin(admin.ModelAdmin):
    list_display = ('cgi_number','date_assigned', 'gr2_unit','name', 'question', )
    list_editable = ['question','date_assigned', 'gr2_unit', 'name']
    ordering = ('cgi_number',)

    class Meta:
        model = CGI
        widgets = {
            'question': forms.TextInput
        }


class CGIResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'cgi', 'progress')
    list_editable = ['progress']
    list_filter = ['student__current_class__classroom', 'cgi', ]
    actions = [add_one, set_zero, set_untested, set_mastered]


admin.site.register(CGI, CGIAdmin)
admin.site.register(CGIResult, CGIResultAdmin)
