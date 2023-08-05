from edc_constants.constants import NOT_APPLICABLE, OTHER, POS

from .constants import (
    BACTERIA,
    CRYPTOCOCCUS_NEOFORMANS,
    ECOLI,
    KLEBSIELLA_SPP,
    NO_GROWTH,
)

BACTERIA_TYPE = (
    (NOT_APPLICABLE, "Not applicable"),
    (ECOLI, "E.coli"),
    (KLEBSIELLA_SPP, "Klebsiella spp."),
    ("streptococcus_pneumoniae", "Streptococcus pneumoniae"),
    ("staphylococus_aureus", "(Sensitive) Staphylococus aureus"),
    ("mrsa", "MRSA"),
    (OTHER, "Other"),
)

BLOOD_CULTURE_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (CRYPTOCOCCUS_NEOFORMANS, "Cryptococcus neoformans"),
    (BACTERIA, "Bacteria"),
    ("bacteria_and_cryptococcus", "Bacteria and Cryptococcus"),
    (OTHER, "Other"),
)

BIOPSY_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (CRYPTOCOCCUS_NEOFORMANS, "Cryptococcus neoformans"),
    ("mycobacterium_tuberculosis", "Mycobacterium Tuberculosis"),
    (OTHER, "Other"),
)

CULTURE_RESULTS = (
    (NOT_APPLICABLE, "Not applicable"),
    (NO_GROWTH, "No growth"),
    (POS, "Positive"),
)

URINE_CULTURE_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (ECOLI, "E.coli"),
    (KLEBSIELLA_SPP, "Klebsiella spp."),
    (OTHER, "Other"),
)

SPUTUM_GENEXPERT = (
    ("mtb_detected_rif_resistance_detected", "MTB DETECTED & Rif Resistance DETECTED"),
    (
        "mtb_detected_rif_resistance_not_detected",
        "MTB DETECTED & Rif Resistance NOT detected",
    ),
    (
        "mtb_detected_rif_resistance_indeterminate",
        "MTB DETECTED & Rif Resistance INDETERMINATE",
    ),
    ("mtb_not_detected", "MTB NOT detected"),
    (NOT_APPLICABLE, "Not applicable"),
)
