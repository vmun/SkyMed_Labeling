from django.apps import AppConfig


class MarkupConfig(AppConfig):
    name = 'markup'

    def ready(self):
        import markup.utils.signals