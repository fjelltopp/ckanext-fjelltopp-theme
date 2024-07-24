import ckan.model as model
from ckan.common import c, request, is_flask_request, g
from datetime import datetime, timedelta
from ckan.plugins import toolkit


def format_locale(locale):
    locale_name = locale.display_name if locale.display_name is not None else locale.english_name
    locale_name = locale_name.replace(' (Portugal)', '').capitalize()
    locale_name = locale_name.replace(' (united kingdom)', '').capitalize()
    return locale_name