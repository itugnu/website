from django.apps import AppConfig


class LectureConfig(AppConfig):
    name = 'lecture'

    def ready(self):
        import lecture.signals  # NOQA
