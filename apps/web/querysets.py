from django.db import models


class StepQuerySet(models.QuerySet):
    def initial(self):
        return self.filter(is_initial=True).first()

    def not_started(self):
        from apps.web.models.step import NOT_STARTED
        return self.filter(status=NOT_STARTED)


class ResponseQuerySet(models.QuerySet):
    def send_message(self, bot, update):
        for response in self.order_by('priority').all():
            response.send_message(bot, update)
