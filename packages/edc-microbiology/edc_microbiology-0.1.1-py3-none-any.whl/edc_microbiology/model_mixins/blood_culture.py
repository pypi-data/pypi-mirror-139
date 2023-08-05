from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import OtherCharField, date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import BACTERIA_TYPE, BLOOD_CULTURE_RESULTS_ORGANISM, CULTURE_RESULTS


class BloodCultureModelMixin(models.Model):

    blood_culture_performed = models.CharField(max_length=5, choices=YES_NO)

    blood_culture_results = models.CharField(
        verbose_name="Blood culture results, if completed",
        max_length=10,
        choices=CULTURE_RESULTS,
        default=NOT_APPLICABLE,
    )

    blood_taken_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    day_blood_taken = models.IntegerField(
        verbose_name="If positive, study day positive culture sample taken",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    blood_culture_organism = models.CharField(
        verbose_name="If growth positive, organism",
        max_length=50,
        choices=BLOOD_CULTURE_RESULTS_ORGANISM,
        default=NOT_APPLICABLE,
    )

    blood_culture_organism_other = OtherCharField(max_length=50, null=True, blank=True)

    bacteria_identified = models.CharField(
        verbose_name="If bacteria, type",
        max_length=50,
        choices=BACTERIA_TYPE,
        default=NOT_APPLICABLE,
    )

    bacteria_identified_other = OtherCharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True
