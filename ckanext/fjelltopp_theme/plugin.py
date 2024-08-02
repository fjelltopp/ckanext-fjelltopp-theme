import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import CKANConfig
import ckanext.fjelltopp_theme.helpers as theme_helpers

log = logging.getLogger(__name__)


class FjelltoppThemePlugin(plugins.SingletonPlugin):
    """An example theme plugin."""

    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def get_helpers(self):
        return {
            'format_locale': theme_helpers.format_locale,
            'get_recently_updated_datasets': theme_helpers.get_recently_updated_datasets,
            'get_last_modifier': theme_helpers.get_last_modifier,
            'get_featured_datasets': theme_helpers.get_featured_datasets,
            'get_datahub_stats': theme_helpers.get_datahub_stats,
            'get_activity_stream_limit': theme_helpers.get_activity_stream_limit,
        }

    def update_config(self, config: CKANConfig):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('assets', 'fjelltopp-theme')
