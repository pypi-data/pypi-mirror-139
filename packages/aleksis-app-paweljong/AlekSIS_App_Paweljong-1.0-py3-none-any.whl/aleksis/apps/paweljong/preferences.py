from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import StringPreference

from aleksis.core.registries import site_preferences_registry

paweljong = Section("paweljong")


@site_preferences_registry.register
class NewsletterChoices(StringPreference):
    section = paweljong
    name = "newsletter_choices"
    default = ""
    required = False
    verbose_name = _("Newsletter choices (comma-seperated)")


@site_preferences_registry.register
class WWSPostUrl(StringPreference):
    section = paweljong
    name = "wws_post_url"
    default = ""
    required = False
    verbose_name = _("POST url for Sympa")
