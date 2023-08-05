from django.apps import apps as django_apps

EDC_MICROBIOLOGY = "EDC_MICROBIOLOGY"
EDC_MICROBIOLOGY_SUPER = "EDC_MICROBIOLOGY_SUPER"
EDC_MICROBIOLOGY_VIEW = "EDC_MICROBIOLOGY_VIEW"

codenames = []
app_config = django_apps.get_app_config("edc_microbiology")
for model_cls in app_config.get_models():
    if "historical" not in model_cls._meta.label_lower:
        for action in ["view_", "add_", "change_", "delete_", "view_historical"]:
            codenames.append(f".{action}".join(model_cls._meta.label_lower.split(".")))
codenames.sort()
