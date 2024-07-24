import ckan.model as model
from ckan.common import c, request, is_flask_request, g
from datetime import datetime, timedelta
from ckan.plugins import toolkit


def format_locale(locale):
    locale_name = locale.display_name if locale.display_name is not None else locale.english_name
    locale_name = locale_name.replace(' (Portugal)', '').capitalize()
    locale_name = locale_name.replace(' (united kingdom)', '').capitalize()
    return locale_name


def get_user_from_id(userid):
    user_show_action = toolkit.get_action('user_show')
    user_info = user_show_action({}, {"id": userid})
    return user_info['fullname']


def get_recently_updated_datasets():
    recently_updated = toolkit.get_action('package_search')(
        data_dict={'q': '*:*', 'sort': 'metadata_modified desc', 'rows': 3})['results']
    return recently_updated[:3]


def get_last_modifier(package_id):
    try:
        package_activity = toolkit.get_action('package_activity_list')(
            data_dict={'id': package_id}
        )
        return get_user_from_id(package_activity[0]['user_id'])
    except Exception:  # TODO: An error is generated, to be investigated, for demo purpose added an exception
        return None


def get_featured_datasets():
    featured_datasets = toolkit.get_action('package_search')(
        data_dict={'fq': 'tags:Featured', 'sort': 'metadata_modified desc', 'rows': 3})['results']
    recently_updated = toolkit.get_action('package_search')(
        data_dict={'q': '*:*', 'sort': 'metadata_modified desc', 'rows': 3})['results']
    datasets = featured_datasets + recently_updated
    return datasets[:3]
