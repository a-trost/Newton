from django.db import models
from django.utils import timezone
from brain.models import StudentRoster
# Create your models here.

class Sticker(models.Model):
    name = models.CharField(max_length=255,)
    slug = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255,)
    image = models.FilePathField(path='static/images/stickers')
    alt_text = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=255, default='CGI')
    order = models.IntegerField(default = 1)

    def image_tag(self):
        return u'<img src="/{}" >'.format(self.image)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return 'Sticker: %s' % self.name

    class Meta:
        ordering = ['category', 'order']


class StickerAssignment(models.Model):
    student = models.ForeignKey(StudentRoster,)
    sticker = models.ForeignKey(Sticker,)
    earned = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'sticker')
        verbose_name = "Earned Sticker"
        verbose_name_plural = "Earned Stickers Assignments"


class Avatar(models.Model):
    '''Student is allowed to set this once a week.
    On the portal page, if kid already set it in the last 6 days, the option won't even appear.'''
    student = models.ForeignKey(StudentRoster)
    date_selected = models.DateTimeField(default=timezone.now)
    sticker = models.ForeignKey(Sticker)

    def image_tag(self):
        return u'<img src="/{}" >'.format(self.sticker.image)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
