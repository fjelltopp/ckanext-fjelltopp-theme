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
        }

    def update_config(self, config: CKANConfig):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('assets', 'fjelltopp-theme')
