""" Core dashboard tag to check if a record is in edition mode
"""

from django import template

from core_main_app.settings import INSTALLED_APPS
if 'core_curate_app' in INSTALLED_APPS:
    import core_curate_app.components.curate_data_structure.api as curate_data_structure_api

register = template.Library()


@register.filter(name='has_draft')
def has_draft(data):
    """Check if if a record is in edition mode.

    Args:
        data:

    Returns:
        Boolean: Is in edition mode

    """
    try:
        # Check if a curate data structure already exists
        curate_data_structure = curate_data_structure_api.get_by_data_id(data['id'])
    except:
        curate_data_structure = None

    return curate_data_structure is not None
