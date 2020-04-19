from django.contrib import admin
from video_encoding.admin import FormatInline

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = (FormatInline,)

    list_dispaly = ('get_filename', 'width', 'height', 'duration')
    fields = ('db_file', 'width', 'height', 'duration')
    readonly_fields = fields
