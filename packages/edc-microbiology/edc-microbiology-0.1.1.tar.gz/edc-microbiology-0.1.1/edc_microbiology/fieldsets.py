def get_urine_culture_fieldset():
    return [
        "Urine Culture (Only for patients with >50 white cells in urine)",
        {
            "fields": (
                "urine_culture_performed",
                "urine_taken_date",
                "urine_culture_results",
                "urine_culture_organism",
                "urine_culture_organism_other",
            )
        },
    ]


def get_blood_culture_fieldset():
    return [
        "Blood Culture",
        {
            "fields": (
                "blood_culture_performed",
                "blood_culture_results",
                "blood_taken_date",
                "day_blood_taken",
                "blood_culture_organism",
                "blood_culture_organism_other",
                "bacteria_identified",
                "bacteria_identified_other",
            )
        },
    ]


def get_sputum_fieldset():
    return [
        "Sputum Microbiology",
        {
            "fields": (
                "sputum_afb_performed",
                "sputum_afb_date",
                "sputum_results_afb",
                "sputum_performed",
                "sputum_taken_date",
                "sputum_results_culture",
                "sputum_results_positive",
                "sputum_genexpert_performed",
                "sputum_genexpert_date",
                "sputum_result_genexpert",
            )
        },
    ]


def get_csf_fieldset():
    return [
        "CSF Microbiology",
        {
            "fields": (
                "csf_genexpert_performed",
                "csf_genexpert_date",
                "csf_result_genexpert",
            )
        },
    ]


def get_histopathology_fieldset():
    return [
        "Histopathology",
        {
            "fields": (
                "tissue_biopsy_taken",
                "tissue_biopsy_results",
                "biopsy_date",
                "day_biopsy_taken",
                "tissue_biopsy_organism",
                "tissue_biopsy_organism_other",
                "histopathology_report",
            )
        },
    ]
