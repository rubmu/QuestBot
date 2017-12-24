import re

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.conditions_parsing import NumericStringParser
from apps.web.models.constants import HookActions
from apps.web.models.update import Update
from apps.web.validators import validate_conditions
from .abstract import TimeStampModel


BUTTON_CLICK = HookActions.BUTTON_CLICK
COMMON_MESSAGE = HookActions.COMMON_MESSAGE
CALLBACK_MESSAGE = HookActions.CALLBACK_MESSAGE

FIELD_CHOICES = (
    (BUTTON_CLICK, _('Button click')),
    (COMMON_MESSAGE, _('Common message')),
    (CALLBACK_MESSAGE, _('Callback message')),
)


class Handler(TimeStampModel):
    step = models.ForeignKey(
        to='Step',
        help_text=_('Handle particular actions for this step'),
        related_name='handlers',
        on_delete=models.CASCADE,
    )
    enabled_on = models.CharField(
        verbose_name=_('Enabled on'),
        help_text=_('Enabled only on following requests'),
        max_length=255,
        choices=FIELD_CHOICES,
        default=BUTTON_CLICK,
    )
    ids_expression = models.CharField(
        max_length=500,
        verbose_name='Mathematics expression',
        help_text=_("Allowed / +*()! /. A set of rules by condition's id"),
        null=True,
        blank=True,
        validators=[validate_conditions]
    )
    allowed = models.ManyToManyField(
        to='AppUser',
        related_name='handlers',
        blank=True,
    )
    step_on_success = models.ForeignKey(
        to='Step',
        verbose_name='Step on success',
        help_text='Move to this step if mathematics expression truthful',
        related_name='true_handlers',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    step_on_error = models.ForeignKey(
        to='Step',
        verbose_name='Step on error',
        help_text='Move to this step if mathematics expression wrongful',
        related_name='false_handlers',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    title = models.CharField(verbose_name="Handler title", max_length=255)

    class Meta:
        verbose_name = _('Handler')
        verbose_name_plural = _('Handlers')

    def __str__(self):
        return ' | '.join([str(self.step.number), self.title, ])

    def check_handler_conditions(
            self,
            update: Update,
            specify_ids: bool = True,
    ) -> bool:
        """Responsible for conditions checking

        Ensure that massage fits in with the condition rules

        """
        conditions = self.conditions

        if self.ids_expression:
            expr = self.ids_expression.replace(' ', '') + ' '
        elif conditions.count():
            expr = '{}' * conditions.count() + ' '
        else:
            return False

        if not re.match('^.*{\d+}.*$', expr):
            specify_ids = False

        cond_result = {
            ''.join(['#', str(i.id)]): int(i.is_match_to_rule(update))
            for i in self.conditions.all()
        }

        formatted_expr = ''
        for i in range(len(expr)-1):
            formatted_expr += expr[i]
            if specify_ids and expr[i] == '{' and expr[i+1].isdigit():
                formatted_expr += '#'

        if specify_ids:
            filled_expr = formatted_expr.format(**cond_result)
        else:
            filled_expr = formatted_expr.format(*list(cond_result.values()))

        nsp = NumericStringParser()
        result = nsp.eval(filled_expr)

        return result > 0
