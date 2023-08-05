from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model import models as edc_models
from edc_model.models import HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from .model_mixins import (
    BloodCultureModelMixin,
    CsfModelMixin,
    HistopathologyModelMixin,
    SputumModelMixin,
    UrineCultureModelMixin,
)


class Microbiology(
    UniqueSubjectIdentifierFieldMixin,
    UrineCultureModelMixin,
    BloodCultureModelMixin,
    SputumModelMixin,
    CsfModelMixin,
    HistopathologyModelMixin,
    SiteModelMixin,
    edc_models.BaseUuidModel,
):

    report_datetime = models.DateTimeField(default=get_utcnow)

    on_site = CurrentSiteManager()
    objects = models.Manager()
    history = HistoricalRecords()

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Microbiology"
        verbose_name_plural = "Microbiology"
