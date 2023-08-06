import copy

from django.apps import apps
from django.db.models import ObjectDoesNotExist
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.settings import FRAMEWORK_PLUGIN_INFO


def get_related_object(scope, field_name):
    """
    Returns the related field, referenced by the content of a ModelChoiceField.
    """
    try:
        Model = apps.get_model(scope[field_name]["model"])
        relobj = Model.objects.get(pk=scope[field_name]["pk"])
    except (ObjectDoesNotExist, LookupError):
        relobj = None
    return relobj


def insert_fields(
    fieldsets, new_fields, block=None, position=-1, blockname=None, blockattrs=None
):
    """
    creates a copy of fieldsets inserting the new fields either in the indexed block at the position,
    or - if no block is given - at the end
    """
    if blockattrs is None:
        blockattrs = dict()
    if block is None:
        fs = (
            list(fieldsets[:position] if position != -1 else fieldsets)
            + [
                (
                    blockname,
                    {
                        "classes": ("collapse",) if len(fieldsets) > 0 else (),
                        "fields": list(new_fields),
                        **blockattrs,
                    },
                )
            ]
            + list(fieldsets[position:] if position != -1 else [])
        )
        return fs
    modify = copy.deepcopy(fieldsets[block])
    fields = modify[1]["fields"]
    if position >= 0:
        modify[1]["fields"] = (
            list(fields[:position]) + list(new_fields) + list(fields[position:])
        )
    else:
        modify[1]["fields"] = (
            list(fields[: position + 1] if position != -1 else fields)
            + list(new_fields)
            + list(fields[position + 1 :] if position != -1 else [])
        )
    fs = (
        list(fieldsets[:block] if block != -1 else fieldsets)
        + [modify]
        + list(fieldsets[block + 1 :] if block != -1 else [])
    )
    return fs


def get_template_path(prefix, template, name):
    return f"djangocms_frontend/{settings.framework}/{prefix}/{template}/{name}.html"


def get_plugin_template(instance, prefix, name, templates):
    template = getattr(instance, "template", templates[0][0])
    template_path = get_template_path(prefix, template, name)

    try:
        select_template([template_path])
    except TemplateDoesNotExist:
        # TODO render a warning inside the template
        template_path = get_template_path(prefix, "default", name)

    return template_path


def first_choice(choices):
    for value, verbose in choices:
        if not isinstance(verbose, (tuple, list)):
            return value
        else:
            first = first_choice(verbose)
            if first is not None:
                return first
    return None


# use mark_safe_lazy to delay the translation when using mark_safe
# otherwise they will not be added to /locale/
# https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#other-uses-of-lazy-in-delayed-translations
mark_safe_lazy = lazy(mark_safe, str)


def link_to_framework_doc(ui_item, topic):
    link = FRAMEWORK_PLUGIN_INFO.get(ui_item, {}).get(topic, None)
    if link:
        return mark_safe_lazy(
            _(
                'Read more in the <a href="{link}" target="_blank">documentation</a>.'
            ).format(link=link)
        )
    return None
