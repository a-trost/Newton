from django.contrib import admin
from .models import TeacherApproval, Score

# Register your models here.




class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject','date')
    search_fields = ['student__first_name', 'student__last_name' ]
    list_filter = ['date', 'student__current_class__classroom', 'student__current_class__grade']

class TeacherApprovalAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'approved')
    list_editable = ('approved',)
    search_fields = ['student__first_name', 'student__last_name',  ]
    list_filter = ['date','approved', 'student__current_class__classroom', 'student__current_class__grade']

admin.site.register(Score, ScoreAdmin)
admin.site.register(TeacherApproval, TeacherApprovalAdmin)