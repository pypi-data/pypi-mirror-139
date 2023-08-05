from edc_model import models as edc_models

from .model_mixins import (
    BloodCultureModelMixin,
    CsfModelMixin,
    HistopathologyModelMixin,
    SputumModelMixin,
    UrineCultureModelMixin,
)


class Microbiology(
    UrineCultureModelMixin,
    BloodCultureModelMixin,
    SputumModelMixin,
    CsfModelMixin,
    HistopathologyModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Microbiology"
        verbose_name_plural = "Microbiology"
