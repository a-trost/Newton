from django.contrib import admin

from .models import Sticker, StickerAssignment, Avatar
# Register your models here.

class StickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'category', 'order', 'image_tag', 'alt_text')
    search_fields = ['name', 'slug', 'description']
    list_editable = ['slug', 'description', 'category', 'alt_text', 'order']
    list_filter = ['category']
    #fields = ('image_tag',)
    #readonly_fields = ('image_tag',)

class StickerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'sticker')
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ('sticker__category','student__current_class__classroom','sticker',)


class AvatarAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_selected', 'sticker', 'image_tag' )
    search_fields = ['student__first_name', 'student__last_name',]

admin.site.register(Sticker, StickerAdmin)
admin.site.register(StickerAssignment, StickerAssignmentAdmin)
admin.site.register(Avatar, AvatarAdmin)
