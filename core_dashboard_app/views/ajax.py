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
from core_dashboard_app import constants

# FIXME: case of uninstall app

def _check_rights_document(request_user_is_staff, request_user_id, document_user):
    """ Check if the user is staff or if the document belongs to the user.

    Args:
        request_user_is_staff:
        request_user_id:
        document_user:

    Returns:
    """
    if not request_user_is_staff and str(request_user_id) != str(document_user):
        raise Exception("You don't have the rights to perform this action.")


def _get_forms(form_ids, request_user_is_staff, request_user_id):
    """ Get all the forms from the list of ids.

    Args:
        form_ids:
        request_user_is_staff:
        request_user_id:

    Returns:
        list form
    """

    list_form = []
    try:
        for form_id in form_ids:
            # Get the form
            form = curate_data_structure_api.get_by_id(form_id)

            # Check the rights
            _check_rights_document(request_user_is_staff, request_user_id, form.user)

            list_form.append(form)
    except DoesNotExist:
        raise Exception('It seems a record is missing. Please refresh the page.')
    except Exception, e:
        raise Exception(e.message)

    return list_form


def _get_data(data_ids, request_user_is_staff, request_user_id):
    """ Get all the data from the list of ids.

    Args:
        data_ids:
        request_user_is_staff:
        request_user_id:

    Returns:
        data table
    """

    data_table = []
    try:
        for data_id in data_ids:

            # Get the data
            data = data_api.get_by_id(data_id)

            # Check the rights
            _check_rights_document(request_user_is_staff, request_user_id, data.user_id)

            data_table.append(data)
    except DoesNotExist:
        raise Exception('It seems a record is missing. Please refresh the page.')
    except Exception, e:
        raise Exception(e.message)

    return data_table


# FIXME: fix error message
def delete_document(request):
    """ Delete a document (record or form).

    Args:
        request:

    Returns:
    """
    document = request.POST['functional_object']

    document_ids = request.POST.getlist('document_id[]', [])
    if len(document_ids) > 1 and not request.user.is_staff:
        return HttpResponseServerError({"You don't have the rights to perform this action."}, status=403)

    if document == constants.FUNCTIONAL_OBJECT_ENUM.RECORD:
        return _delete_record(request, document_ids)
    elif document == constants.FUNCTIONAL_OBJECT_ENUM.FORM:
        return _delete_form(request, document_ids)

    return HttpResponseBadRequest({"Bad entries. Please check the parameters."})


def _delete_form(request, form_ids):
    """ Delete forms.

        Args:
            request:
            form_ids:

        Returns:
        """
    try:
        list_form = _get_forms(form_ids, request.user.is_staff, request.user.id)
    except Exception, e:
        messages.add_message(request, messages.INFO, e.message)
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    try:
        for form in list_form:
            curate_data_structure_api.delete(form)
        messages.add_message(request, messages.INFO, 'Form deleted with success.')
    except:
        messages.add_message(request, messages.INFO, 'A problem occurred while deleting.')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def _delete_record(request, data_ids):
    """ Delete records.

    Args:
        request:
        data_ids:

    Returns:
    """

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


def change_owner_document(request):
    """ Change owner of a document (record or form).

    Args:
        request:

    Returns:
    """

    if 'document_id[]' in request.POST and 'user_id' in request.POST and 'functional_object' in request.POST:
        document = request.POST['functional_object']
        user_id = request.POST['user_id']

        document_ids = request.POST.getlist('document_id[]', [])
        if len(document_ids) > 1 and not request.user.is_staff:
            return HttpResponseServerError({"You don't have the rights to perform this action."}, status=403)

        if document == constants.FUNCTIONAL_OBJECT_ENUM.RECORD:
            return _change_owner_record(request, document_ids, user_id)
        elif document == constants.FUNCTIONAL_OBJECT_ENUM.FORM:
            return _change_owner_form(request, document_ids, user_id)

    else:
        return HttpResponseBadRequest({"Bad entries. Please check the parameters."})

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def _change_owner_form(request, form_ids, user_id):
    """ Change the owner of a form.

    Args:
        request:
        data_ids:
        user_id:

    Returns:
    """
    try:
        list_form = _get_forms(form_ids, request.user.is_staff, request.user.id)
    except Exception, e:
        messages.add_message(request, messages.INFO, e.message)
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    try:
        for form in list_form:
            form.user = user_id
            curate_data_structure_api.upsert(form)
        messages.add_message(request, messages.INFO, 'Owner changed with success.')
    except Exception, e:
        messages.add_message(request, messages.INFO, "Something wrong occurred during the change of owner.")

    return HttpResponse(json.dumps({}), content_type='application/javascript')


# FIXME: fix error message
def _change_owner_record(request, data_ids, user_id):
    """ Change the owner of a record.

    Args:
        request:
        data_ids:
        user_id:

    Returns:
    """
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

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def edit_record(request):
    """ Edit a record.

    Args:
        request:

    Returns:
    """
    try:
        data = data_api.get_by_id(request.POST['id'])
    except DoesNotExist:
        return HttpResponseServerError({"It seems a record is missing."}, status=404)

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
                                                form_string=data.xml_content,
                                                data=data)
    curate_data_structure = curate_data_structure_api.upsert(curate_data_structure)

    return HttpResponse(json.dumps({'url': reverse("core_curate_enter_data", args=(curate_data_structure.id,))}),
                        content_type='application/javascript')
