""" Ajax API
"""
import json

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
import core_main_app.components.data.api as data_api
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_main_app.commons.exceptions import DoesNotExist


def _get_data(data_ids, request_user_is_staff, request_user_id):
    """
    Get all the data from the list of ids

    Args: data_ids:
          request_user_is_staff:
          request_user_id:
    Returns: data table
    """

    data_table = []
    try:
        for data_id in data_ids:
            data = data_api.get_by_id(data_id)
            if not request_user_is_staff and request_user_id != data.user_id:
                raise Exception("You don't have the rights to perform this action.")
            data_table.append(data)
    except DoesNotExist:
        raise Exception('It seems a record is missing. Please refresh the page.')

    return data_table


# FIXME: fix error message
def delete_record(request):
    """
        Deletes a data.

    Args: request:
    Returns:
    """
    data_ids = request.POST.getlist('record_id[]', [])
    if len(data_ids) > 1 and not request.user.is_staff:
        return HttpResponseServerError({"You don't have the rights to perform this action."}, status=500)

    try:
        list_data = _get_data(data_ids, request.user.is_staff, request.user.id)
    except Exception, e:
        messages.add_message(request, messages.INFO, e.message)
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    try:
        for data in list_data:
            data_api.delete(data)
        messages.add_message(request, messages.INFO, 'Record deleted with success.')
    except:
        messages.add_message(request, messages.INFO, 'A problem occurred while deleting.')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


# FIXME: fix error message
def change_owner_record(request):
    """
        Changes the owner of a record.

    Args: request:
    Returns:
    """
    if 'recordID[]' in request.POST and 'userID' in request.POST:
        data_ids = request.POST.getlist('recordID[]', [])
        user_id = request.POST['userID']

        if len(data_ids) > 1 and not request.user.is_staff:
            return HttpResponseServerError({"You don't have the rights to perform this action."}, status=500)

        try:
            list_data = _get_data(data_ids, request.user.is_staff, request.user.id)
        except Exception, e:
            messages.add_message(request, messages.INFO, e.message)
            return HttpResponse(json.dumps({}), content_type='application/javascript')
        try:
            for data in list_data:
                data.user_id = user_id
                data_api.upsert(data)
            messages.add_message(request, messages.INFO, 'Owner changed with success.')
        except Exception, e:
            messages.add_message(request, messages.INFO, "Something wrong occurred during the change of owner.")
    else:
        return HttpResponseBadRequest({"Bad entries. Please check the parameters."})

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def core_dashboard_edit_record(request):
    """
        Edit a record.

    Args: request:
    Returns:
    """
    try:
        data = data_api.get_by_id(request.POST['id'])
    except DoesNotExist:
        return HttpResponseServerError({"It seems a record is missing."}, status=500)

    try:
        # Check if a curate data structure already exists
        curate_data_structure = curate_data_structure_api.get_by_user_id_and_template_id_and_name(
                                                                                    user_id=str(request.user.id),
                                                                                    template_id=str(data.template.id),
                                                                                    name=data.title)
        if curate_data_structure is not None:
            curate_data_structure_api.delete(curate_data_structure)
    except DoesNotExist:
        pass
    except Exception, e:
        return HttpResponseServerError({"A problem occurred while editing."}, status=500)

    # Create a new curate data structure
    curate_data_structure = CurateDataStructure(user=str(request.user.id),
                                                template=str(data.template.id),
                                                name=data.title,
                                                form_string=data.xml_file,
                                                data=data)
    curate_data_structure = curate_data_structure_api.upsert(curate_data_structure)

    return HttpResponse(json.dumps({'url': reverse("core_curate_enter_data", args=(curate_data_structure.id,))}),
                        content_type='application/javascript')
