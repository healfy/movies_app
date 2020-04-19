from datetime import datetime
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings
from video_encoding.fields import VideoField
from video_encoding.models import Format

from .managers import BaseManager


class BaseModel(models.Model):

    created_at = models.DateTimeField(verbose_name='Time of created',
                                      default=datetime.now,
                                      db_index=True)

    updated_at = models.DateTimeField(verbose_name='Time of last update',
                                      null=True,
                                      blank=True)

    deleted_at = models.DateTimeField(verbose_name='Time then row was deleted',
                                      null=True,
                                      blank=True)

    is_deleted = models.BooleanField(verbose_name='Is deleted row',
                                     default=False)

    objects = BaseManager()
    all_objects = models.Manager()

    BASE_FIELDS = ('deleted_at', 'updated_at', 'is_deleted')

    def save(self, **kwargs):
        self.updated_at = datetime.now()
        super().save(**kwargs)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.is_deleted = True
        self.save()

    def __repr__(self):
        return "<Model{} ({})>".format(self.__class__.__name__, self.id)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Movie(BaseModel):
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)
    duration = models.FloatField(editable=False, null=True)
    format_set = GenericRelation(Format)
    db_file = VideoField(width_field='width', height_field='height',
                         duration_field='duration')

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    @property
    def mp4(self):
        return self.format_set.filter(format='mp4_sd').last()

    @property
    def webm(self):
        return self.format_set.filter(format='webm_sd').last()
