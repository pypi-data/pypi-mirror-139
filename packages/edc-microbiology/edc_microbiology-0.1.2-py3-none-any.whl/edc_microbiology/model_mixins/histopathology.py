from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import OtherCharField, date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import BIOPSY_RESULTS_ORGANISM, CULTURE_RESULTS


class HistopathologyModelMixin(models.Model):

    tissue_biopsy_taken = models.CharField(max_length=5, choices=YES_NO)

    tissue_biopsy_results = models.CharField(
        verbose_name="If YES, results",
        max_length=10,
        choices=CULTURE_RESULTS,
        default=NOT_APPLICABLE,
    )

    biopsy_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    day_biopsy_taken = models.IntegerField(
        verbose_name="If positive, Study day positive culture sample taken",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    tissue_biopsy_organism = models.CharField(
        verbose_name="If growth positive, organism",
        max_length=50,
        choices=BIOPSY_RESULTS_ORGANISM,
        default=NOT_APPLICABLE,
    )

    tissue_biopsy_organism_other = OtherCharField(max_length=50, null=True, blank=True)

    histopathology_report = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
