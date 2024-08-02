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
    package_activity = toolkit.get_action('package_activity_list')(
        data_dict={'id': package_id}
    )
    return get_user_from_id(package_activity[0]['user_id'])


def get_featured_datasets():
    featured_datasets = toolkit.get_action('package_search')(
        data_dict={'fq': 'tags:Featured', 'sort': 'metadata_modified desc', 'rows': 3})['results']
    recently_updated = toolkit.get_action('package_search')(
        data_dict={'q': '*:*', 'sort': 'metadata_modified desc', 'rows': 3})['results']
    datasets = featured_datasets + recently_updated
    return datasets[:3]


def get_datahub_stats(**kwargs):
    stats = toolkit.h.get_site_statistics()

    total_datasets = {'label': 'Total datasets', 'value': stats['dataset_count']}
    org = {'label': 'Teams', 'value': stats['organization_count']}
    group = {'label': 'Categories', 'value': stats['group_count']}

    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week_as_str = start_of_week.strftime('%Y-%m-%dT%H:%M:%SZ')

    data_dict = {
        'q': '*:*',
        'fq': 'state:active AND metadata_modified:[{} TO NOW]'.format(start_of_week_as_str),
        'rows': 0
    }

    result = toolkit.get_action('package_search')({}, data_dict)
    datasets_updated_this_week = {'label': 'Updated this week', 'value': result.get('count', 0)}

    users_list = toolkit.get_action('user_list')({})
    active_users = len([user for user in users_list if user['state'] == 'active'])
    active_users = {'label': 'Users', 'value': active_users}

    valid_values = []
    for key, value in kwargs.items():
        if isinstance(value, dict) and \
                'label' in value and isinstance(value['label'], str) and \
                'value' in value and isinstance(value['value'], float):
            valid_values.append(value)

    return [
        total_datasets,
        datasets_updated_this_week,
        active_users,
        org,
        group,
    ] + valid_values




def get_activity_stream_limit():
    base_limit = toolkit.config.get("ckan.activity_list_limit")
    max_limit = toolkit.config.get("ckan.activity_list_limit_max")
    return min(base_limit, max_limit)
