import string
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from google.appengine.ext import db
import models
from models import CustomFormSettings
import view_common
import common


def get_common_client_form_fields(request, client):
    cf_settings = CustomFormSettings.GetSettings(request=request)
    curr_client_referrer = None
    curr_client_reason_for_visit = None
    if client:
        curr_client_referrer = client.referrer
        curr_client_reason_for_visit = client.reason_for_visit
    return {'referrer_choices': cf_settings.get_referrer_choices(),
            'curr_client_referrer': curr_client_referrer,
            'reason_for_visit_choices':
            cf_settings.get_reason_for_visit_choices(),
            'curr_client_reason_for_visit': curr_client_reason_for_visit,
            'new_client_script': cf_settings.get_new_client_script()
            }


def add_client_form(request):
    if request.method == 'POST':
        form = models.ClientForm(request.POST)
        if form.is_valid():
            entity = models.ClientInfo(**form.cleaned_data)
            view_common.save_entity(request, entity)
            return HttpResponseRedirect(reverse('show_client'))
    else:
        form = models.ClientForm()
    render_to_response_dict = {
        "form": form,
        "submit_link": reverse('add_client'),
    }
    render_to_response_dict.update(get_common_client_form_fields(request,
                                                                 None))
    return render_to_response("add_client_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def add_client_standalone(request):
    if request.method == 'POST':
        form = models.SimpleClientForm(request.POST)
        if form.is_valid():
            form_dict = form.cleaned_data
            form_dict['client_status'] = 'Active'
            entity = models.ClientInfo(**form.cleaned_data)
            view_common.save_entity(request, entity)
            json_data = json.dumps({"key": str(entity.get_id()),
                                    'name': unicode(entity)})
            return HttpResponse(json_data, mimetype="application/json")
    else:
        form = models.SimpleClientForm()
    render_to_response_dict = {
        "form": form,
        "submit_link": reverse('add_client_standalone'),
    }
    render_to_response_dict.update(get_common_client_form_fields(request,
                                                                 None))
    return render_to_response(
        "add_client_standalone_template.html",
        render_to_response_dict, context_instance=RequestContext(request))


def update_client(request, client_id):
    client = models.ClientInfo.safe_get_by_id(int(client_id), request)
    # TODO: actually show an error message instead of just redirecting
    if not client:
        view_common.log_access_violation('update_client')
        return HttpResponseRedirect(reverse('show_client'))
    if request.method == 'POST':
        form = models.ClientForm(request.POST)
        if form.is_valid():
            client.update_model(form.cleaned_data)
            view_common.save_entity(request, client)
            return HttpResponseRedirect(client.get_absolute_url())
    else:
        client_dict = db.to_dict(client)
        for key in client_dict:
            value = client_dict[key]
            field = models.EncryptedField(value)
            try:
                client_dict[key] = field.make_value_from_datastore(value)
            except TypeError:
                pass
        form = models.ClientForm(initial=client_dict)
    render_to_response_dict = {
        "form": form,
        "submit_link": reverse(update_client, kwargs={'client_id': client_id}),
    }
    render_to_response_dict.update(get_common_client_form_fields(request,
                                                                 client))
    return render_to_response("add_client_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def get_letter_link_list(client_list):
    client_letters = set()
    for client in client_list:
        item_string = client.lastname.upper()
        if item_string and item_string != 'None':
            client_letters.add(item_string[0])
    letter_link_list = []
    for letter in string.ascii_uppercase:
        if letter in client_letters:
            letter_link_list.append((True, letter))
        else:
            letter_link_list.append((False, letter))
    return letter_link_list


def show_client(request):
    client_list = models.ClientInfo.safe_all(request=request).fetch(
        common.get_maximum_num_dos_fetch())
    letter_link_list = get_letter_link_list(client_list)
    render_to_response_dict = {
        "client_list": client_list,
        "letters": letter_link_list,
    }
    return render_to_response("show_client_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def show_client_letter(request, letter):
    client_list = models.ClientInfo.safe_all(request=request).fetch(
        common.get_maximum_num_dos_fetch())
    letter_link_list = get_letter_link_list(client_list)
    client_letter_list = []
    for client in client_list:
        if client.lastname:
            if string.lower(client.lastname[0]) == string.lower(letter):
                client_letter_list.append(client)
    render_to_response_dict = {
        "client_list": client_letter_list,
        "letters": letter_link_list,
    }
    return render_to_response("show_client_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def get_amount_owed(running_balance_list, dos):
    balance = 0.0
    for individual_dos in dos:
        try:
            if individual_dos.amt_due:
                balance += float(individual_dos.amt_due)
        except (ValueError, TypeError):
            pass
        try:
            if individual_dos.adjustment:
                balance += float(individual_dos.adjustment)
        except (ValueError, TypeError):
            pass
        try:
            if individual_dos.amt_paid:
                balance -= float(individual_dos.amt_paid)
        except (ValueError, TypeError):
            pass
        running_balance_list.append(balance)

    return balance


def dos_sort(dos):
    return dos.get_starttime()


def get_common_dos_fields(request, client, curr_dos=None):
    dos = models.DOS.safe_all(request=request)
    dos = dos.filter('clientinfo =', client.key()).fetch(
        common.get_maximum_num_dos_fetch())
    dos = sorted(dos, key=dos_sort)

    running_balance_list = []
    balance = get_amount_owed(running_balance_list, dos)
    dos_zipped = zip(dos, running_balance_list)

    cf_settings = CustomFormSettings.GetSettings(request=request)
    curr_session_type_choices = None
    if curr_dos:
        curr_session_type_choices = curr_dos.session_type
    return {'session_type_choices': cf_settings.get_session_type_choices(),
            'curr_session_type_choices': curr_session_type_choices,
            "dos_zipped": dos_zipped,
            "balance": balance}


def show_specific_client(request, client_id):
    client = models.ClientInfo.safe_get_by_id(int(client_id), request=request)
    # TODO: actually show an error message instead of just redirecting
    if not client:
        view_common.log_access_violation('show_specific_client')
        return HttpResponseRedirect(reverse('show_client'))
    if request.method == 'POST':
        form = models.DOSFormNoClientSelect(request.POST)
        if form.is_valid():
            form_dict = form.cleaned_data
            form_dict['clientinfo'] = client
            entity = models.DOS(**form_dict)
            entity = view_common.save_entity(request, entity)
            return HttpResponseRedirect(client.get_absolute_url())
    else:
        form = models.DOSFormNoClientSelect()
    render_to_response_dict = {
                               "client": client,
                               "dos_form": form,
                               "form_dest": client.get_absolute_url(),
                               "dos_id": None,
                               "form_button": "Insert New DOS",
                               }
    render_to_response_dict.update(get_common_dos_fields(request, client))
    return render_to_response("show_specific_client_template.html",
                              render_to_response_dict,
                               context_instance=RequestContext(request))


def update_dos(request, dos_id):
    dos = models.DOS.safe_get_by_id(int(dos_id), request=request)
    # TODO: actually show an error message instead of just redirecting
    if not dos:
        view_common.log_access_violation('update_dos')
        return HttpResponseRedirect(reverse('show_client'))
    client = dos.clientinfo
    if request.method == 'POST':
        form = models.DOSFormNoClientSelect(request.POST,
                                            initial=db.to_dict(dos))
        if form.is_valid():
            dos.update_model(form.cleaned_data)
            view_common.save_entity(request, dos)
            return HttpResponseRedirect(client.get_absolute_url())
    else:
        form = models.DOSFormNoClientSelect(initial=db.to_dict(dos))
    render_to_response_dict = {
        "client": client,
        "dos_form": form,
        "form_dest": dos.get_absolute_url(),
        "dos_id": int(dos_id),
        "form_button": "Update DOS",
    }
    render_to_response_dict.update(get_common_dos_fields(request, client,
                                                         curr_dos=dos))

    return render_to_response("show_specific_client_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def dos_receipt(request, dos_id):
    dos = models.DOS.safe_get_by_id(int(dos_id), request=request)
    # TODO: actually show an error message instead of just redirecting
    if not dos:
        view_common.log_access_violation('update_dos')
        return HttpResponseRedirect(reverse('show_client'))
    client = dos.clientinfo
    form = models.DOSFormNoClientSelect()

    render_to_response_dict = {
        "client": client,
        "dos_form": form,
        "form_dest": client.get_absolute_url(),
        "dos_id": None,
        "form_button": "Insert DOS",
    }
    render_to_response_dict.update(get_common_dos_fields(request, client))

    view_common.add_popup(render_to_response_dict,
                          models.Invoice.GetInvoice(request, dos_id))

    return render_to_response("show_specific_client_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def search(request):
    if request.method == 'POST':
        form = models.SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('%sclient-list?search=%s' % (
                common.get_mwa_root(), form.cleaned_data['search_input']))
    else:
        form = models.SearchForm()
    render_to_response_dict = {
        "form": form,
    }

    return render_to_response("search_template.html", render_to_response_dict,
                              context_instance=RequestContext(request))


def search_result(request, search_input):
    search_clients = models.ClientInfo.safe_all(request=request)
    client_list = []
    search_input_chunks = search_input.split()
    search_input_chunks = [string.lower(chunk)
                           for chunk in search_input_chunks]
    for client in search_clients:
        for search_input_chunk in search_input_chunks:
            if search_input_chunk in string.lower(str(client.getallfields())):
                client_list.append(client)
                break
    render_to_response_dict = {
        "client_list": client_list,
    }

    return render_to_response("show_client_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def delete_client(request, client_id):
    client_id = int(client_id)
    client = models.ClientInfo.safe_get_by_id(client_id, request)
    if not client:
        #TODO: Show an error message to the user
        view_common.log_access_violation('delete_client')
        return HttpResponseRedirect(reverse('show_client'))
    if request.method == 'POST':
        common.delete_client(client)
        json_data = json.dumps({"message": 'Success'})
        return HttpResponse(json_data, mimetype="application/json")
    return render_to_response('delete_client.html', {'client': client},
                              context_instance=RequestContext(request))


def get_referrer(client):
    return client.referrer


def get_dsm_code(client):
    return client.dsm_code


def javascript_object_text(text):
    return '"%s",' % view_common.escape_json(text)


def autocomplete(request, model, field, get_field_func):
    model_list = model.safe_all(request=request).filter(
       '%s !=' % field, None).fetch(common.get_maximum_num_dos_fetch())

    field_list = map(get_field_func, model_list)
    # remove duplicates
    field_list = list(set(field_list))
    field_list.sort()
    #field_list now contains all the possible options for this field

    term = request.GET.get('term', '')
    # Create a list with all objects which match the current term the user has
    # typed.
    term_list = [indiv_field for indiv_field in field_list
                 if term in indiv_field]
    term_list.append('----------')
    field_list = term_list + field_list
    response_str = '['
    # optimization: calling join and map are very fast...
    response_str += ''.join(map(javascript_object_text, field_list))
    response_str = response_str.rstrip()
    response_str = response_str.rstrip(',')
    response_str += '\n]'
    return HttpResponse(response_str, mimetype='application/json')


def referrer_autocomplete(request):
    return autocomplete(request, models.ClientInfo, 'referrer', get_referrer)


def dsm_code_autocomplete(request):
    return autocomplete(request, models.ClientInfo, 'dsm_code', get_dsm_code)


def client_balance(request, client_id):
    client = models.ClientInfo.safe_get_by_id(int(client_id), request=request)
    # TODO: actually show an error message instead of just redirecting
    if not client:
        view_common.log_access_violation('show_specific_client')
    dos = models.DOS.safe_all(request=request)
    dos = dos.filter('clientinfo =', client.key()).fetch(
        common.get_maximum_num_dos_fetch())

    balance = get_amount_owed([], dos)
    return HttpResponse(json.dumps({'balance': balance}),
                         mimetype="application/json")
