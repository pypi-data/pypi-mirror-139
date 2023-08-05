from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple

from .fieldsets import (
    get_blood_culture_fieldset,
    get_csf_fieldset,
    get_histopathology_fieldset,
    get_sputum_fieldset,
    get_urine_culture_fieldset,
)


class MicrobiologyModelAdminMixin:

    fieldsets = (
        get_urine_culture_fieldset(),
        get_blood_culture_fieldset(),
        get_sputum_fieldset(),
        get_csf_fieldset(),
        get_histopathology_fieldset(),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "urine_culture_performed": admin.VERTICAL,
        "urine_culture_results": admin.VERTICAL,
        "urine_culture_organism": admin.VERTICAL,
        "blood_culture_performed": admin.VERTICAL,
        "blood_culture_results": admin.VERTICAL,
        "blood_culture_organism": admin.VERTICAL,
        "bacteria_identified": admin.VERTICAL,
        "sputum_afb_performed": admin.VERTICAL,
        "sputum_results_afb": admin.VERTICAL,
        "sputum_performed": admin.VERTICAL,
        "sputum_results_culture": admin.VERTICAL,
        "sputum_result_genexpert": admin.VERTICAL,
        "sputum_genexpert_performed": admin.VERTICAL,
        "csf_result_genexpert": admin.VERTICAL,
        "csf_genexpert_performed": admin.VERTICAL,
        "tissue_biopsy_taken": admin.VERTICAL,
        "tissue_biopsy_results": admin.VERTICAL,
        "tissue_biopsy_organism": admin.VERTICAL,
    }
