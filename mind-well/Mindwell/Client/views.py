import calendar
import datetime
import logging
import operator
import string
import sys
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db
if 'reportlab.zip' not in sys.path:
    sys.path.insert(0, 'reportlab.zip')
import reportlab.lib
import reportlab.platypus
import reportlab.rl_config
import common
import models
import view_common


def change_user(request, change_user=None):
    if change_user is not None:
        next_url = request.META.get('HTTP_REFERER', None) or '/'
        http_response = HttpResponseRedirect(next_url)
        if change_user != 'Self':
            try:
                models.UserPermission().safe_get(change_user)
                http_response.set_cookie('current_user', value=change_user)
            except db.BadKeyError:
                view_common.log_access_violation('change_user')
        else:
            http_response.delete_cookie('current_user')
        return http_response
    return HttpResponseRedirect('/')


def redirect_to_base(request):
    response = HttpResponseRedirect('/Mindwell/show_client/')
    return response


def reports(request):
    return render_to_response("reports_template.html", {},
                              context_instance=RequestContext(request))


def invoices(request):
    form = None
    if request.method == 'POST':
        form = models.InvoiceForm(request.POST, request=request)
        if form.is_valid():
            form_dict = form.cleaned_data
            try:
                client = models.ClientInfo.safe_get_by_id(
                   int(form.cleaned_data['clientinfo']), request=request)
                form_dict['clientinfo'] = client
                entity = models.Invoice(**form_dict)
                view_common.save_entity(request, entity)
                return HttpResponseRedirect(entity.get_absolute_url())
            except ValueError:   # catches calling int on non integer
                logging.exception('Invalid client')
        else:
            logging.error('invoices form is invalid %s' % form)
    if not form:
        form = models.InvoiceForm(request=request)
    all_invoices = models.Invoice.safe_all(request=request).fetch(
        common.get_maximum_num_dos_fetch())
    view_common.prefetch_refprops(all_invoices, models.Invoice.clientinfo)
    for invoice in all_invoices:
        try:
            invoice.clientinfo
            invoice.clientinfo_valid = True
        except db.ReferencePropertyResolveError:
            logging.exception('Deleting invoice without a valid clientinfo')
            db.delete(invoice)
            invoice.clientinfo_valid = False
    all_invoices = [invoice for invoice in all_invoices
                    if invoice.clientinfo_valid]
    render_to_response_dict = {
        "form": form,
        "all_invoices": all_invoices,
    }
    return render_to_response("invoices_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def get_last_day_of_month(curr_date):
    if curr_date.month == 12:
        month = 1
        year = curr_date.year + 1
    else:
        month = curr_date.month + 1
        year = curr_date.year
    return (
        datetime.datetime(year, month, 1, hour=23, minute=59) -
        datetime.timedelta(days=1))


def generate_invoices_dict(start_date, end_date, request=None):
    dos = models.DOS.safe_all(request=request).filter(
        'dos_datetime >=', start_date).filter('dos_datetime <=', end_date)
    invoice_list = []
    client_list = []
    for d in dos:
        if d.get_blocked_time():
            continue
        if str(d.clientinfo.key()) in client_list:
            continue
        else:
            client_list.append(str(d.clientinfo.key()))
        find_invoices = models.Invoice.safe_all(
            request=request, keys_only=True).filter(
                'clientinfo =', d.clientinfo.key()).filter(
                'start_date =', start_date.date()).filter(
                'end_date =', end_date.date())
        if find_invoices.count() > 0:
            invoice_list.append(find_invoices[0])
            continue
        invoice = models.Invoice(clientinfo=d.clientinfo,
            start_date=start_date.date(),
            end_date=end_date.date())
        invoice.userinfo = models.pull_current_user_from_request(request)
        invoice = invoice.put()
        invoice_list.append(invoice)
    invoices = models.Invoice.safe_all(request=request).filter(
        'start_date =', start_date.date()).filter(
        'end_date =', end_date.date())
    all_invoices = models.Invoice.safe_all(request=request)
    form = models.InvoiceForm(request=request)
    render_to_response_dict = {
        "invoices": invoices,
        "start_date": start_date,
        "end_date": end_date,
        "all_invoices": all_invoices,
        "form": form
    }
    return render_to_response_dict


def generate_client_invoices(request, year, month):
    year = int(year)
    month = int(month)
    start_date = datetime.datetime(year, month, 1)
    end_date = get_last_day_of_month(start_date)
    render_to_response_dict = generate_invoices_dict(start_date,
        end_date, request=request)
    return render_to_response("generate_client_invoices_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def generate_client_invoices_by_date(request,
    start_year, start_month, start_day,
    end_year, end_month, end_day):
    start_date = datetime.datetime(year=int(start_year),
                                   month=int(start_month),
                                   day=int(start_day))
    end_date = datetime.datetime(year=int(end_year), month=int(end_month),
                                 day=int(end_day))
    end_date = end_date.replace(hour=23, minute=59)
    render_to_response_dict = generate_invoices_dict(start_date, end_date,
                                                     request=request)

    return render_to_response("generate_client_invoices_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def get_dos_balance(dos):
    dos_balance = 0
    for individual_dos in dos:
        try:
            amt_due = float(individual_dos.amt_due)
        except (ValueError, TypeError):
            amt_due = 0
        try:
            adjustment = float(individual_dos.adjustment)
        except (ValueError, TypeError):
            adjustment = 0
        try:
            amt_paid = float(individual_dos.amt_paid)
        except (ValueError, TypeError):
            amt_paid = 0
        dos_balance = dos_balance + (amt_due - amt_paid + adjustment)
    return dos_balance


def DOSInvoiceHeader():
    return [
        ['Date of Service',
        'CPT Code',
        'Length of Session',
        'Amount Due',
        'Amount Paid',
        'Adjustment',
        'Type of Payment', ]
    ]


def DOSInvoiceRow(dos):
    return (
        dos.get_dos_date_display(),
        str(dos.session_type),
        str(dos.get_duration()),
        str(dos.amt_due),
        str(dos.amt_paid),
        str(dos.adjustment),
        str(dos.type_pay)
    )

PAGE_HEIGHT = reportlab.rl_config.defaultPageSize[1]
PAGE_WIDTH = reportlab.rl_config.defaultPageSize[0]


class MyPDFClass(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.text_mode = 'left'
        self.font_size = 16
        self.font_name = 'Times-Roman'
        self.y_pos = PAGE_HEIGHT - (.5 * reportlab.lib.units.inch)

    def set_text_mode(self, text_mode):
        self.text_mode = text_mode

    def set_font_name(self, font_name):
        self.font_name = font_name
        self.__update_font()

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.__update_font()

    def __update_font(self):
        self.canvas.setFont(self.font_name, self.font_size)

    def __draw_text(self, line):
        if self.text_mode == 'left':
            self.canvas.drawString(reportlab.lib.units.inch * .5, self.y_pos,
                                   line)
        if self.text_mode == 'right':
            self.canvas.drawRightString(
                PAGE_WIDTH - reportlab.lib.units.inch * .5, self.y_pos, line)
        if self.text_mode == 'center':
            self.canvas.drawCentredString(PAGE_WIDTH / 2, self.y_pos, line)
        if self.text_mode == 'line':
            self.canvas.line(1, self.y_pos, PAGE_WIDTH, self.y_pos)
        if self.text_mode == 'line_sig':
            self.canvas.line(reportlab.lib.units.inch * .5, self.y_pos,
                             PAGE_WIDTH / 3, self.y_pos)

    def move_to_bottom(self, margin):
        self.y_pos = margin

    def add_text(self, text):
        new_text = text.replace('\r', '')
        for line in new_text.split('\n'):
            self.__draw_text(line)
            self.y_pos -= self.font_size


def render_invoice_pdf(request, invoice_dict):
    PAGE_HEIGHT = reportlab.rl_config.defaultPageSize[1]
    PAGE_WIDTH = reportlab.rl_config.defaultPageSize[0]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = ('attachment; filename=invoice_%s.pdf' %
                                       str(invoice_dict['invoice'].key().id()))
    header_text = (
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
      {'text_mode': 'left', 'font': 'Times-Bold', 'font_size': 16,
       'text': invoice_dict['invoice_settings'].practice_name},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size':  12,
       'text': invoice_dict['invoice_settings'].header},
      {'text_mode': 'line', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
      {'text_mode': 'right', 'font': 'Times-Roman', 'font_size': 12,
       'text': invoice_dict['invoice_settings'].right_header},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
      {'text_mode': 'right', 'font': 'Times-Roman', 'font_size': 12,
       'text': 'Invoice Number: %s' % str(invoice_dict['invoice'].key().id())},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': 'Name: %s %s' % (
        str(invoice_dict['invoice'].clientinfo.firstname),
        str(invoice_dict['invoice'].clientinfo.lastname))},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': 'Address: %s %s\n%s %s %s' % (
        invoice_dict['invoice'].clientinfo.address,
        invoice_dict['invoice'].clientinfo.address2,
        invoice_dict['invoice'].clientinfo.city,
        invoice_dict['invoice'].clientinfo.state,
        invoice_dict['invoice'].clientinfo.zipcode)},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
      {'text_mode': 'right', 'font': 'Times-Roman', 'font_size': 12,
       'text': 'ICD 10: %s\n' % invoice_dict['dsm_code']},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
    )
    footer_text = (
      {'text_mode': 'line_sig', 'font': 'Times-Roman', 'font_size': 12,
       'text': ''},
      {'text_mode': 'left', 'font': 'Times-Roman', 'font_size': 12,
       'text': invoice_dict['invoice_settings'].footer},
    )

    def calculate_top_margin():
        margin = .5 * reportlab.lib.units.inch
        for text_entry in header_text:
            new_text = text_entry['text'].replace('\r', '')
            for unused_line in new_text.split('\n'):
                margin += text_entry['font_size']
        return margin

    def calculate_bottom_margin():
        margin = .5 * reportlab.lib.units.inch
        for text_entry in footer_text:
            new_text = text_entry['text'].replace('\r', '')
            for unused_line in new_text.split('\n'):
                margin += text_entry['font_size']
        return margin

    # First we import some constructors, some paragraph styles and other
    # conveniences from other modules.
    def myFirstPage(canvas, doc):
        canvas.saveState()
        my_pdf = MyPDFClass(canvas)
        for text_entry in header_text:
            my_pdf.set_text_mode(text_entry['text_mode'])
            my_pdf.set_font_name(text_entry['font'])
            my_pdf.set_font_size(text_entry['font_size'])
            my_pdf.add_text(text_entry['text'])
        my_pdf.move_to_bottom(calculate_bottom_margin())
        for text_entry in footer_text:
            my_pdf.set_text_mode(text_entry['text_mode'])
            my_pdf.set_font_name(text_entry['font'])
            my_pdf.set_font_size(text_entry['font_size'])
            my_pdf.add_text(text_entry['text'])
        canvas.restoreState()

    doc = reportlab.platypus.SimpleDocTemplate(response)
    doc.bottomMargin = (calculate_bottom_margin() +
                        (.5 * reportlab.lib.units.inch))
    doc.height = 10 * reportlab.lib.units.inch
    doc.topMargin = calculate_top_margin()
    doc.pagesize = (595.27, 841.89)
    # doc.pagesize=(595.27,500)
    Story = []
    styles = reportlab.lib.styles.getSampleStyleSheet()
    style = styles["Normal"]
    my_list = DOSInvoiceHeader()
    my_list += map(DOSInvoiceRow, invoice_dict['dos'])
    t = reportlab.platypus.Table(my_list)
    t.setStyle(reportlab.platypus.TableStyle([
      ('BOX', (0, 0), (-1, -1), 0.25, reportlab.lib.colors.black),
      ('INNERGRID', (0, 0), (-1, -1), 0.25, reportlab.lib.colors.black),
      ('FONTSIZE', (0, 0), (-1, 0), 10)
    ]))
    Story.append(t)
    Story.append(reportlab.platypus.Paragraph(
        'Balance: %d' % get_dos_balance(invoice_dict['dos']), style))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myFirstPage)
    return response


def invoice_display(request, invoice_id, all_dos='', attended_only='',
                    html=False):

    invoice = models.Invoice.safe_get_by_id(int(invoice_id), request)
    if not invoice:
        return HttpResponseRedirect('/Mindwell/show_client/')
    dos = models.DOS.safe_all(request=request)
    invoice_enddatetime = datetime.datetime(
        invoice.end_date.year,
        invoice.end_date.month,
        invoice.end_date.day,
        hour=23,
        minute=59)

    dos = dos.filter(
      'clientinfo =', invoice.clientinfo.key()).filter(
      'dos_datetime >=', invoice.start_date).filter(
      'dos_datetime <=', invoice_enddatetime)
    if attended_only:
        dos = dos.filter('session_result IN ', ['Attended', 'Attended, Not Billed'])
    dos = dos.fetch(common.get_maximum_num_dos_fetch())
    dos_balance = 0
    dsm_code = invoice.clientinfo.dsm_code
    for individual_dos in dos:
        try:
            amt_due = float(individual_dos.amt_due)
        except (ValueError, TypeError):
            amt_due = 0
        try:
            adjustment = float(individual_dos.adjustment)
        except (ValueError, TypeError):
            adjustment = 0
        try:
            amt_paid = float(individual_dos.amt_paid)
        except (ValueError, TypeError):
            amt_paid = 0
        dos_balance = dos_balance + (amt_due - amt_paid + adjustment)
        if not dsm_code:
            dsm_code = individual_dos.dsm_code
    invoice_settings_entity = models.InvoiceSettings.safe_all(request=request)
    if invoice_settings_entity.count() > 0:
        invoice_settings = invoice_settings_entity[0]
    else:
        invoice_settings = models.InvoiceSettings(practice_name='', header='',
                                           right_header='', footer='')
    if html:
        return render_to_response('invoice_display_template.html',
          {
            "invoice": invoice,
            "dos": dos,
            "dos_balance": dos_balance,
            "dsm_code": dsm_code,
            "invoice_settings": invoice_settings,
        }, context_instance=RequestContext(request))
    else:
        return render_invoice_pdf(request, {
            "invoice": invoice,
            "dos": dos,
            "dos_balance": dos_balance,
            "dsm_code": dsm_code,
            "invoice_settings": invoice_settings,
        })


def provider_invoices(request):
    if request.method == 'POST':
        form = models.DailyInvoiceForm(request.POST)
        if form.is_valid():
            start_invoice_date = form.cleaned_data.get('start_invoice_date')
            end_invoice_date = form.cleaned_data.get('end_invoice_date')
            new_url = reverse('provider_invoices_display', kwargs={
                'start_year': '%04d' % int(start_invoice_date.year),
                'start_month': '%02d' % int(start_invoice_date.month),
                'start_day': '%02d' % int(start_invoice_date.day),
                 'end_year': '%04d' % int(end_invoice_date.year),
                 'end_month': '%02d' % int(end_invoice_date.month),
                 'end_day': '%02d' % int(end_invoice_date.day)})
            return HttpResponseRedirect(new_url)
    else:
        form = models.DailyInvoiceForm()
    render_to_response_dict = {
        "form": form,
    }
    return render_to_response('provider_invoices_template.html',
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def provider_invoices_display(request, start_year, start_month, start_day,
                              end_year, end_month, end_day):
    start_invoice_date = datetime.datetime(
        year=int(start_year), month=int(start_month), day=int(start_day))
    end_invoice_date = datetime.datetime(
        year=int(end_year), month=int(end_month), day=int(end_day))
    end_invoice_date = end_invoice_date.replace(hour=23, minute=59)
    dos = models.DOS.safe_all(request=request).filter(
        'dos_datetime >=', start_invoice_date).filter(
        'dos_datetime <=', end_invoice_date).fetch(
        common.get_maximum_num_dos_fetch())
    check_total = 0
    cash_total = 0
    total = 0
    other_total = 0
    non_blocked_dos = [d for d in dos if not d.get_blocked_time()]
    for d in non_blocked_dos:
        if d.amt_paid:
            try:
                if 'cash' in string.lower(str(d.type_pay)):
                    cash_total += float(d.amt_paid)
                elif 'check' in string.lower(str(d.type_pay)):
                    check_total += float(d.amt_paid)
                else:
                    other_total += float(d.amt_paid)
                total += float(d.amt_paid)
            except (ValueError, TypeError):
                pass

    render_to_response_dict = {
        "dos": non_blocked_dos,
        "cash_total": cash_total,
        "check_total": check_total,
        "other_total": other_total,
        "total": total,
    }
    return render_to_response("provider_invoices_display_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def provider_statistics(request):
    this_year = datetime.date.today().year
    years = range(this_year - 5, this_year + 10)
    render_to_response_dict = {
        "years": years,
    }
    return render_to_response('provider_statistics_template.html',
                              render_to_response_dict,
                               context_instance=RequestContext(request))


def provider_statistics_display(request, year):

    start_invoice_date = datetime.datetime(year=int(year), month=int(1),
        day=int(1))
    end_invoice_date = datetime.datetime(year=int(year), month=int(12),
        day=int(31))
    end_invoice_date = end_invoice_date.replace(hour=23, minute=59)
    dos = models.DOS.safe_all(request=request).filter(
        'dos_datetime >=', start_invoice_date).filter(
        'dos_datetime <=', end_invoice_date).fetch(
        common.get_maximum_num_dos_fetch())
    view_common.prefetch_refprops(dos, models.DOS.clientinfo)
    monthly_count = [0 for unused_x in range(0, 12)]
    month_value = [0 for unused_x in range(0, 12)]
    month_number = ['%02d' % x for x in range(1, 13)]
    for d in dos:
        if d.get_blocked_time():
            continue
        monthly_count[d.dos_datetime.month - 1] += 1
        if d.amt_paid:
            try:
                month_value[d.dos_datetime.month - 1] += float(d.amt_paid)
            except (ValueError, TypeError):
                pass
    render_to_response_dict = {
        "months": zip(month_number, calendar.month_name[1:13],
            monthly_count, month_value)
    }
    render_to_response_dict.update(get_provider_stats(dos))

    return render_to_response("provider_statistics_display_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def get_provider_stats(dos):
    dos_dict = {}
    # remove all except for attended and with real clients
    dos = [d for d in dos
           if not d.get_blocked_time() and (
               d.session_result == 'Attended' or
               d.session_result == 'Attended, Not Billed'
           )]
    for d in dos:
        if models.DOS.clientinfo.get_value_for_datastore(d) in dos_dict:
            dos_dict[models.DOS.clientinfo.get_value_for_datastore(d)] += 1
        else:
            dos_dict[models.DOS.clientinfo.get_value_for_datastore(d)] = 1
    try:
        max_sessions = max(dos_dict.iteritems(), key=operator.itemgetter(1))[1]
    except ValueError:
        max_sessions = 0
    max_sess_list = [0] * (max_sessions)
    for dos_key in dos_dict:
        max_sess_list[dos_dict[dos_key] - 1] += 1
    total = 0
    number_clients = 0
    for sess in range(0, len(max_sess_list)):
        total += max_sess_list[sess] * (sess + 1)
        number_clients += max_sess_list[sess]
    if number_clients:
        average = float(total) / number_clients
    else:
        average = 0
    stats_dict = {
        'session_list': max_sess_list,
        'average': average,
    }
    return stats_dict


def provider_stats_all_time(request):
    dos = models.DOS.safe_all(request=request).filter(
        'session_result IN ', ['Attended', 'Attended, Not Billed']).fetch(
        common.get_maximum_num_dos_fetch())
    render_to_response_dict = get_provider_stats(dos)

    return render_to_response('provider_stats_all_time_template.html',
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def export_provider_data(request):
    return render_to_response('export_provider_data_template.html', {},
                              context_instance=RequestContext(request))


def OutputInfoHeader(instance):
    text = ''
    for field_desc, unused_field in instance.getallfields_inc_hidden():
        text += '"%s",' % field_desc
    text += '\n'
    return text


def OutputInfo(instance):
    text = ''
    for unused_field_desc, field in instance.getallfields_inc_hidden():
        text += '"%s",' % field
    text += '\n'
    return text


def run_export_provider_data(request):
    client_list = models.ClientInfo.safe_all(request=request)
    text = ''
    try:
        text += OutputInfoHeader(client_list[0])
    except IndexError:
        pass
    text += ''.join(map(OutputInfo, client_list))

    text += '\n'
    dos = models.DOS.safe_all(request=request)
    try:
        text += OutputInfoHeader(dos[0])
    except IndexError:
        pass
    text += ''.join(map(OutputInfo, dos))
    response = HttpResponse(text, mimetype='text/csv')
    response['Content-Disposition'] = (
        'attachment;  filename=mindwell_exported_data.csv')
    return response


def settings(request):
    return render_to_response('settings_template.html', {},
                              context_instance=RequestContext(request))


def permission_settings(request, update=''):
    # don't let someone change permissions of user they are acting as
    if (users.get_current_user() !=
        models.pull_current_user_from_request(request)):
        return HttpResponseRedirect('/Mindwell/show_client/')

    # explicity only allow changing
    user_permissions = models.UserPermission.safe_all(request=None)
    permission_requests = models.UserPermission.get_permission_requests()
    form = models.UserPermissionForm()

    render_to_response_dict = {
        "form": form,
        "user_permissions": user_permissions,
        "permission_requests": permission_requests,
        "update": update,
    }

    return render_to_response('permission_settings_template.html',
                              render_to_response_dict,
                              context_instance=RequestContext(request))


@view_common.prevent_acting_as
def update_permission_settings(request):
    if request.method == 'POST':
        form = models.UserPermissionForm(request.POST)
        if form.is_valid():
            entity = models.UserPermission(**form.cleaned_data)
            view_common.save_entity(request, entity)
    return HttpResponseRedirect(reverse('updated_permission_settings',
                                        kwargs={'update': 'update'}))


def delete_permission(request, permission_id):

    permission = models.UserPermission.safe_get_by_id(permission_id)
    if permission:
        db.delete(permission)
    return HttpResponseRedirect('/Mindwell/settings/permission')


@view_common.prevent_acting_as
def update_permission_requests(request, request_permission_id):
    # explicity only allow changing
    user_permissions = models.UserPermission.safe_all(request=None)
    permission_requests = models.UserPermission.get_permission_requests()
    form = models.UserPermissionForm()
    request_to_update = models.UserPermission.unsafe_get(request_permission_id)
    if not request_to_update:
        view_common.log_access_violation('update_permission_requests')
        # show error message to user
        return HttpResponseRedirect('/Mindwell/show_client/')

    request_form = models.UserPermissionRequestsForm(
        initial=db.to_dict(request_to_update))
    render_to_response_dict = {
        "form": form,
        "request_form": request_form,

        "user_permissions": user_permissions,
        "permission_requests": permission_requests,
        "request_to_update": request_to_update,
        "request_permission_id": request_permission_id,

    }
    return render_to_response('permission_settings_template.html',
                              render_to_response_dict,
                              context_instance=RequestContext(request))


@view_common.prevent_acting_as
def update_request_settings(request, request_permission_id):
    request_to_update = models.UserPermission.unsafe_get(request_permission_id)
    if not request_to_update:
        view_common.log_access_violation('update_request_settings')
        # show error message to user
        return HttpResponseRedirect('/Mindwell/show_client/')
    if request.method == 'POST':
        form = models.UserPermissionRequestsForm(request.POST)
        if form.is_valid():
            request_to_update.update_model(form.cleaned_data)
            request_to_update.put()
    return HttpResponseRedirect(reverse('updated_permission_settings',
                                        kwargs={'update': 'update'}))


def generic_singleton_update(request, model_class, form_class, update=''):
    form = None
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            entity = model_class.Get(request)
            if entity:
                entity.update_model(form.cleaned_data)
            else:
                entity = model_class(**form.cleaned_data)
            view_common.save_entity(request, entity)
            return HttpResponseRedirect(entity.get_saved_url())
    if not form:
        entity = model_class.Get(request)
        if entity:
            form = form_class(initial=db.to_dict(entity))
        else:
            form = form_class.get_default_form()

    render_to_response_dict = {
        "form": form,
        "update": update,
    }
    return render_to_response(form.get_edit_template(),
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def invoice_settings(request, update=''):
    return generic_singleton_update(request, models.InvoiceSettings,
                                    models.InvoiceSettingsForm,
                                    update)


def calendar_settings(request, update=''):
    return generic_singleton_update(request, models.CalendarSettings,
                                    models.CalendarSettingsForm,
                                    update)


def custom_form_settings(request, update=''):
    return generic_singleton_update(request, models.CustomFormSettings,
                                    models.CustomFormSettingsForm,
                                    update)


def administrator(request):
    if request.method == 'POST':
        form = models.UserInfoForm(request.POST)
        if form.is_valid():
            entity = models.UserInfo(**form.cleaned_data)
            entity.put()
            memcache.delete('userlist')
            return HttpResponseRedirect('/administrator/')

    form = models.UserInfoForm()

    render_to_response_dict = {
        "form": form,
    }

    return render_to_response("administrator_template.html",
                              render_to_response_dict,
                              context_instance=RequestContext(request))


def clear_memcache(request):
    memcache.delete('userlist')
    return HttpResponseRedirect('/administrator/')


def admin_update_all_dos(request):
    dos_list = models.DOS.all()
    for dos in dos_list:
        dos.put()
    return HttpResponseRedirect('/administrator/')


def admin_update_some_dos(request, num_entities=100):
    num_entities = int(num_entities)
    entity_list = models.DOS.all().filter('meta_version !=',
                                          models.dos_meta_version)
    update_list = []
    counter = 0
    for dos in entity_list:
        counter += 1
        if counter > num_entities:
            break
        dos.meta_version = models.dos_meta_version
        if not dos.user_id:
            dos.user_id = dos.userinfo.user_id()
        update_list.append(dos)
    db.put(update_list)
    return HttpResponseRedirect('/administrator/')


def admin_change_email(request, old_email, new_email, num_entities=100):
    entity_list = models.ClientInfo.all().filter('userinfo =',
                                                 users.User(old_email))
    if entity_list.count() == 0:
        logging.info('Changing models.DOS')
        entity_list = models.DOS.all().filter('userinfo =',
                                              users.User(old_email))
    if entity_list.count() == 0:
        logging.info('Changing models.UserPermission')
        entity_list = models.UserPermission.all().filter('userinfo =',
                                                         users.User(old_email))
    if entity_list.count() == 0:
        logging.info('Changing models.Invoice')
        entity_list = models.Invoice.all().filter('userinfo =',
                                                  users.User(old_email))
    if entity_list.count() == 0:
        logging.info('Changing models.InvoiceSettings')
        entity_list = models.InvoiceSettings.all().filter(
            'userinfo =', users.User(old_email))
    if entity_list.count() == 0:
        logging.info('Changing models.CalendarSettings')
        entity_list = models.CalendarSettings.all().filter(
            'userinfo =', users.User(old_email))
    put_future_list = []
    count = 0
    for entity in entity_list:
        entity.userinfo = users.User(new_email)
        put_future_list.append(db.put_async(entity))
        count += 1
        if count >= num_entities:
            break
    for put_future in put_future_list:
        put_future.get_result()
    logging.info("%s %s %d" % (old_email, new_email, count))
    return HttpResponseRedirect('/administrator/')
