# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from lecture.models import Lecture
from common.models import User


test_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)


class LectureTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="tester@itugnu.org", username="tester")

    def test_lecture(self):
        lecture_name = "Test Lecture"
        lecture = Lecture.objects.create(
            name=lecture_name,
            description='Some lecture description.',
            lecturer=self.user,
            classroom='EEB0000',
            start_date=timezone.datetime(year=1994, month=4, day=8, hour=9),
            end_date=timezone.datetime(year=3001, month=5, day=28, hour=18),
            is_registration_open=True
        )
        lecture.poster = SimpleUploadedFile('test.gif', test_gif, content_type='image/gif')
        lecture.save()
        self.assertEqual(lecture.__str__(), lecture_name)
        self.assertEqual(lecture.weeks, 52549)
        self.assertIn('/media/lectures/{pk}/test'.format(pk=lecture.pk), lecture.poster.url)
