from djangocms_frontend.helpers import get_related_object

try:
    from functools import cached_property
except ImportError:  # Only available since Pyhton 3.8
    cached_property = property

from django.utils.translation import gettext_lazy as _
from django.utils.translation import ungettext

from djangocms_frontend.models import FrontendUIItem

from .constants import GRID_CONTAINER_CHOICES


class GridContainer(FrontendUIItem):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True
        verbose_name = _("Container")
        _("GridContainer")

    def get_short_description(self):
        text = ""
        for item in GRID_CONTAINER_CHOICES:
            if item[0] == self.container_type:
                text = item[1]
        return f"({text})"

    @cached_property
    def image(self):
        if getattr(self, "container_image", False):
            return get_related_object(self.config, "container_image")
        return None


class GridRow(FrontendUIItem):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True
        verbose_name = _("Row")
        _("GridRow")

    def get_short_description(self):
        column_count = len(self.child_plugin_instances or [])
        column_count_str = ungettext(
            "(1 column)", "(%(count)i columns)", column_count
        ) % {"count": column_count}

        return column_count_str


class GridColumn(FrontendUIItem):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True
        verbose_name = _("Column")
        _("GridColumn")

    def get_short_description(self):
        text = ""
        if self.xs_col:
            text += f"(col-{self.xs_col}) "
        else:
            text += "(auto) "
        return text.strip()
