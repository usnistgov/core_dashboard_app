""" Ajax API
"""
import json

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

import core_main_app.components.data.api as data_api
import core_main_app.components.user.api as user_api
from core_dashboard_app import constants
from core_main_app.commons.exceptions import DoesNotExist, LockError
from core_main_app.components.blob import api as blob_api
from core_main_app.components.lock.api import is_object_locked
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.components.workspace import api as workspace_api
if 'core_curate_app' in INSTALLED_APPS:
    from core_curate_app.components.curate_data_structure.models import CurateDataStructure
    import core_curate_app.components.curate_data_structure.api as curate_data_structure_api


def _check_rights_document(request_user_is_superuser, request_user_id, document_user):
    """ Check if the user is superuser or if the document belongs to the user.

    Args:
        request_user_is_superuser:
        request_user_id:
        document_user:

    Returns:
    """
    if not request_user_is_superuser and str(request_user_id) != str(document_user):
        raise Exception("You don't have the rights to perform this action.")


def _get_workspaces(workspace_ids, request_user_is_superuser, request_user_id):
    """ Get all the workspaces from the list of ids.

    Args:
        workspace_ids:
        request_user_is_superuser:
        request_user_id:

    Returns:
        list form
    """

    list_workspaces = []
    try:
        for workspace_id in workspace_ids:
            # Get the workspace
            workspace = workspace_api.get_by_id(workspace_id)

            list_workspaces.append(workspace)
    except DoesNotExist:
        raise Exception('It seems a workspace is missing. Please refresh the page.')
    except Exception, e:
        raise Exception(e.message)

    return list_workspaces


def _get_blobs(blob_ids, request_user_is_superuser, request_user_id):
    """ Get all the blobs from the list of ids.

    Args:
        blob_ids:
        request_user_is_superuser:
        request_user_id:

    Returns:
        list form
    """

    list_blobs = []
    try:
        for blob_id in blob_ids:
            # Get the blob
            blob = blob_api.get_by_id(blob_id)

            # Check the rights
            _check_rights_document(request_user_is_superuser, request_user_id, blob.user_id)

            list_blobs.append(blob)
    except DoesNotExist:
        raise Exception('It seems a blob is missing. Please refresh the page.')
    except Exception, e:
        raise Exception(e.message)

    return list_blobs


def _get_forms(form_ids, request_user_is_superuser, request_user_id):
    """ Get all the forms from the list of ids.

    Args:
        form_ids:
        request_user_is_superuser:
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
            _check_rights_document(request_user_is_superuser, request_user_id, form.user)

            list_form.append(form)
    except DoesNotExist:
        raise Exception('It seems a record is missing. Please refresh the page.')
    except Exception, e:
        raise Exception(e.message)

    return list_form


def _get_data(data_ids, user):
    """ Get all the data from the list of ids.

    Args:
        data_ids:
        user:

    Returns:
        data table
    """

    data_table = []
    try:
        for data_id in data_ids:

            # Get the data
            data = data_api.get_by_id(data_id, user)

            # Check the rights
            _check_rights_document(user.is_superuser, str(user.id), data.user_id)

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
    if len(document_ids) > 1 and not request.user.is_superuser:
        return HttpResponseServerError({"You don't have the rights to perform this action."}, status=403)

    if document == constants.FUNCTIONAL_OBJECT_ENUM.RECORD:
        return _delete_record(request, document_ids)
    elif document == constants.FUNCTIONAL_OBJECT_ENUM.FORM:
        return _delete_form(request, document_ids)
    elif document == constants.FUNCTIONAL_OBJECT_ENUM.FILE:
        return _delete_file(request, document_ids)
    elif document == constants.FUNCTIONAL_OBJECT_ENUM.WORKSPACE:
        return _delete_workspace(request, document_ids)

    return HttpResponseBadRequest({"Bad entries. Please check the parameters."})


def _delete_workspace(request, workspace_ids):
    """ Delete workspace.

        Args:
            request:
            workspace_ids:

        Returns:
        """
    try:
        list_workspaces = _get_workspaces(workspace_ids, request.user.is_superuser, request.user.id)
    except Exception, e:
        messages.add_message(request, messages.INFO, e.message)
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    try:
        for workspace in list_workspaces:
            workspace_api.delete(workspace, request.user)
    except AccessControlError, ace:
        return HttpResponseBadRequest(ace.message)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def _delete_file(request, blob_ids):
    """ Delete blobs.

        Args:
            request:
            blob_ids:

        Returns:
        """
    try:
        list_blob = _get_blobs(blob_ids, request.user.is_superuser, request.user.id)
    except Exception, e:
        messages.add_message(request, messages.INFO, e.message)
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    try:
        for blob in list_blob:
            blob_api.delete(blob)
        messages.add_message(request, messages.INFO, 'File deleted with success.')
    except:
        messages.add_message(request, messages.INFO, 'A problem occurred while deleting.')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def _delete_form(request, form_ids):
    """ Delete forms.

        Args:
            request:
            form_ids:

        Returns:
        """
    try:
        list_form = _get_forms(form_ids, request.user.is_superuser, request.user.id)
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
        list_data = _get_data(data_ids, request.user)
    except Exception, e:
        messages.add_message(request, messages.INFO, e.message)
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    try:
        for data in list_data:
            data_api.delete(data, request.user)
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
        if len(document_ids) > 1 and not request.user.is_superuser:
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
        list_form = _get_forms(form_ids, request.user.is_superuser, request.user.id)
    except Exception, e:
        return HttpResponseBadRequest(e.message)

    try:
        for form in list_form:
            form.user = user_id
            curate_data_structure_api.upsert(form)
    except Exception, e:
        return HttpResponseBadRequest(e.message)

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
        list_data = _get_data(data_ids, request.user)
    except Exception, e:
        return HttpResponseBadRequest(e.message)
    try:
        new_user = user_api.get_user_by_id(user_id)
        for data in list_data:
            data_api.change_owner(data, new_user, request.user)
    except Exception, e:
        return HttpResponseBadRequest(e.message)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def edit_record(request):
    """ Edit a record.

    Args:
        request:

    Returns:
    """
    try:
        data = data_api.get_by_id(request.POST['id'], request.user)
    except DoesNotExist:
        return HttpResponseServerError({"It seems a record is missing."}, status=404)

    try:
        # Check if a curate data structure already exists
        curate_data_structure = curate_data_structure_api.get_by_data_id(data.id)
    except DoesNotExist:
        # Create a new curate data structure
        curate_data_structure = CurateDataStructure(user=str(request.user.id),
                                                    template=str(data.template.id),
                                                    name=data.title,
                                                    form_string=data.xml_content,
                                                    data=data)
        curate_data_structure = curate_data_structure_api.upsert(curate_data_structure)
    except Exception, e:
        return HttpResponseServerError({"A problem occurred while editing."}, status=500)

    return HttpResponse(json.dumps({'url': reverse("core_curate_enter_data",
                                                   args=(curate_data_structure.id,))}),
                        content_type='application/javascript')
