from django.contrib import admin
from .models import *


# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'date')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Note, NoteAdmin)
admin.site.register(Tag, TagAdmin)
