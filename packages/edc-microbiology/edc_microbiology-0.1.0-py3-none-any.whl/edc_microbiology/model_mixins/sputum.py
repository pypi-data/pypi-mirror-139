from django.db import models
from edc_constants.choices import POS_NEG_NA, YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_microbiology.choices import SPUTUM_GENEXPERT
from edc_model.models import date_not_future
from edc_protocol.validators import date_not_before_study_start


class SputumModelMixin(models.Model):

    sputum_afb_performed = models.CharField(
        verbose_name="AFB microscopy performed?",
        max_length=5,
        choices=YES_NO,
        help_text="Was sputum AFB done?",
    )

    sputum_afb_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    sputum_results_afb = models.CharField(
        verbose_name="AFB results",
        max_length=10,
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
    )

    sputum_performed = models.CharField(
        verbose_name="Culture performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sputum_taken_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    sputum_results_culture = models.CharField(
        verbose_name="Culture results",
        max_length=10,
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
    )

    sputum_results_positive = models.CharField(
        verbose_name="If culture is positive, please specify:",
        max_length=50,
        null=True,
        blank=True,
    )

    sputum_genexpert_performed = models.CharField(
        verbose_name="Sputum Gene-Xpert performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sputum_genexpert_date = models.DateField(
        verbose_name="Date sputum Gene-Xpert taken",
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True,
    )

    sputum_result_genexpert = models.CharField(
        verbose_name="Sputum Gene-Xpert results",
        max_length=45,
        choices=SPUTUM_GENEXPERT,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
