# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.db.models.signals import pre_save
from django.dispatch import receiver
from lecture.models import Lecture


@receiver(pre_save, sender=Lecture)
def lecture_pre_save(sender, instance, *args, **kwargs):
    """Delete old poster image if exists."""
    if instance.pk:
        old_lecture = Lecture.objects.get(pk=instance.pk)
        # If new poster has different name
        if old_lecture.poster and instance.poster and old_lecture.poster.name != instance.poster.name:
            pre_save.disconnect(lecture_pre_save, sender=sender)
            old_lecture.poster.delete()
            pre_save.connect(lecture_pre_save, sender=sender)
        # If poster is removed
        elif old_lecture.poster and not instance.poster:
            pre_save.disconnect(lecture_pre_save, sender=sender)
            old_lecture.poster.delete()
            pre_save.connect(lecture_pre_save, sender=sender)
