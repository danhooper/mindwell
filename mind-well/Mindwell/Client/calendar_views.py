import logging
import common
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from google.appengine.ext import db
import datetime
import models
from models import CustomFormSettings
import view_common


def Javascript_Object_DOS(dos):
    try:
        return """
{
"id":%d,
"title":"%s",
"start":"%s",
"end":"%s",
"allDay":false,
"url":"%s",
"note":"%s",
"description":"%s",
"backgroundColor":"%s",
"borderColor":"%s",
"textColor":"%s"
},
            """ % (
                dos.get_id(),
                view_common.escape_json(unicode(dos)),
                dos.get_starttime().isoformat('T'),
                dos.get_endtime().isoformat('T'),
                dos.get_calendar_absolute_url(),
                view_common.escape_json(dos.get_note()),
                view_common.escape_json(dos.get_hover_tip()),
                dos.get_background_color(), dos.get_background_color(),
                dos.get_text_color()
            )
    except:
        logging.exception('Exception in Javascript_Object_DOS')
        return ''


class CalendarFeed(object):
    def __init__(self, request, starttime, endtime):
        self.request = request
        self.starttime = starttime
        self.endtime = endtime
        self.dos_recurr_list = []
        self.__run_filters()
        self.__GetAllDOS()
        self.__PopulateDOSRecurr()

    def __run_filters(self):
        # limiting this to 3000 allows 3000 events in a month or ~100 per day
        self.dos_list = models.DOS.safe_all(request=self.request).filter(
            'dos_datetime >', self.starttime).filter(
            'dos_datetime <', self.endtime)
        # Get all models.DOS with an end date for the repeating
        self.dos_repeats = models.DOS.safe_all(request=self.request).filter(
            'dos_repeat_end_date >=', self.starttime).fetch(
            common.get_maximum_num_dos_fetch())
        # Get All models.DOS without a repeat end date
        self.dos_repeats += models.DOS.safe_all(request=self.request).filter(
            'dos_repeat !=', 'No').filter('dos_repeat_end_date =', None).fetch(
            common.get_maximum_num_dos_fetch())
        self.dos_list = self.dos_list.fetch(common.get_maximum_num_dos_fetch())

    def __GetAllDOS(self):
        view_common.prefetch_refprops(self.dos_list + self.dos_repeats,
                                      models.DOS.clientinfo)

    def __build_dos_recurr_list(self):
#        view_common.prefetch_refprops(self.dos_repeats, models.DOS.clientinfo)
        for dos in self.dos_repeats:
            if int(dos.get_repeat_freq()) == 0:
                continue
            tempdate = dos.dos_datetime
            repeat_timedelta = datetime.timedelta(
                days=int(dos.get_repeat_freq()))
            while tempdate < self.starttime:
                tempdate += repeat_timedelta

            repeat_end_date = (dos.get_repeat_end_date() +
                datetime.timedelta(days=1))
            while tempdate < self.endtime and tempdate < repeat_end_date:
                if not self.__DOSInThisSlot(tempdate, dos):
                    new_dos = models.DOSRecurr(dos_base=dos)
                    new_dos.dos_recurr_datetime = tempdate
                    self.dos_recurr_list.append(new_dos)
                tempdate += repeat_timedelta

    # note we create models.DOSRecurr objects here but never bother saving
    # them. so the models.DOSRecurr model in models.py is just used to store
    # helper functionality
    def __PopulateDOSRecurr(self):
        self.__build_dos_recurr_list()
        view_common.prefetch_refprops(
            [dos.dos_base for dos in self.dos_recurr_list],
            models.DOS.clientinfo)

    def __DOSInThisSlot(self, timeslot, new_dos):
        for dos in self.dos_list:
            if timeslot == dos.dos_datetime:
                if (new_dos.clientinfo and dos.clientinfo and
                    new_dos.clientinfo.key() == dos.clientinfo.key()):
                    return True
                if not new_dos.clientinfo and not dos.clientinfo:
                    return True
        for dos in self.dos_recurr_list:
            if timeslot == dos.dos_recurr_datetime:
                if (new_dos.clientinfo and dos.dos_base.clientinfo and
                    new_dos.clientinfo.key() == dos.dos_base.clientinfo.key()):
                    return True
                if not new_dos.clientinfo and not dos.dos_base.clientinfo:
                    return True
        return False

    def GetFeed(self):
        response_str = '['
        # optimization: calling join and map are very fast...
        response_str += ''.join(map(Javascript_Object_DOS, self.dos_list))
        response_str += ''.join(map(Javascript_Object_DOS,
                                    self.dos_recurr_list))
        response_str = response_str.rstrip()
        response_str = response_str.rstrip(',')
        response_str += '\n]'
        return response_str


class CalendarLinks(object):
    def __init__(self, weekdate=datetime.datetime.today()):
        self.weekdate = weekdate

    def get_absolute_url(self):
        return reverse('calendar_date',
                       kwargs={'year': '%04d' % self.weekdate.year,
                               'month': '%02d' % self.weekdate.month,
                               'day': '%02d' % self.weekdate.day})

    def get_receipt_absolute_url(self, dos_id):
        return reverse('calendar_print_receipt',
                       kwargs={'year': '%04d' % self.weekdate.year,
                               'month': '%02d' % self.weekdate.month,
                               'day': '%02d' % self.weekdate.day,
                               'receipt_dos': dos_id})


class Link(object):
    def __init__(self, link=None, link_name=None, cssclass=None):
        self.link = link
        self.link_name = link_name
        self.cssclass = cssclass

    def get_absolute_url(self):
        return self.link

    def __unicode__(self):
        return self.link_name


def handle_calendar_display_post(request, calendar_links):
    form = models.DOSForm(request.POST, request=request)
    if form.is_valid():
        form_dict = form.cleaned_data
        try:
            client = models.ClientInfo.safe_get_by_id(
                int(form.cleaned_data['clientinfo']), request=request)
            form_dict['clientinfo'] = client
        except ValueError:  # catches calling int on non integer
            form_dict['clientinfo'] = None
        entity = models.DOS(**form_dict)
        entity = view_common.save_entity(request, entity)
        print_receipt = form.cleaned_data.get('print_receipt')
        if print_receipt:
            receipt_url = calendar_links.get_receipt_absolute_url(
                int(entity.get_id()))
            return HttpResponseRedirect(receipt_url)
        return HttpResponseRedirect(calendar_links.get_absolute_url())
    else:
        logging.info(form.errors)


def calendar_display(request, year=None, month=None, day=None, hour=None,
                     minute=None, dos_id=None, dos_recurr_id=None,
                     receipt_dos=None):
    invoice = models.Invoice.GetInvoice(request, receipt_dos)
    if year and month and day:
        request_date = datetime.datetime(int(year), int(month), int(day))
    else:
        request_date = datetime.datetime.today()
        calendar_links = CalendarLinks(request_date)
        return HttpResponseRedirect(calendar_links.get_absolute_url())
    calendar_links = CalendarLinks(request_date)
    #pdb.set_trace()
    form = None
    if request.method == 'POST':
        response = handle_calendar_display_post(request, calendar_links)
        if response:
            return response
    links = []
    blocked_time = False
    submit_link = request.path
    dos = True
    if dos_id:
        dos = models.DOS.safe_get_by_id(int(dos_id), request)
    elif dos_recurr_id:
        dos = models.DOS.safe_get_by_id(int(dos_recurr_id), request)
    if not dos:
        view_common.log_access_violation('calendar_display')
        # TODO: show an error message
        return HttpResponseRedirect(reverse('calendar'))
    if hour is not None and minute is not None:
        dos_datetime = datetime.datetime(int(year), int(month), int(day),
                                         int(hour), int(minute), 0, 0)
        form = models.DOSForm(request=request, initial={
           'dos_datetime': dos_datetime,
           'dos_endtime':
           (dos_datetime + datetime.timedelta(minutes=45)).time()
           })
        if dos_id:
            # if this is an old dos without an endtime then add one
            # (previously a duration was the method of determining the end
            #  time)
            if not dos.dos_endtime:
                dos.dos_endtime = dos.get_endtime().time()
            initial_dict = db.to_dict(dos)
            if dos.clientinfo:
                initial_dict['clientinfo'] = dos.clientinfo.get_id()
            form = models.DOSForm(request=request, initial=initial_dict)
            submit_link = dos.get_update_absolute_url()
            links.append(Link(link=dos.get_delete_absolute_url(),
                              link_name='Delete this DOS'))
        elif dos_recurr_id:
            dosrecurr = models.DOSRecurr(dos_base=dos)
            links.append(Link(link=dos.get_cancel_all_series_url(dos_datetime),
                              link_name='Cancel all in series'))
            form = dosrecurr.get_DOSForm(request, dos_datetime)
        if dos_id or dos_recurr_id:
            blocked_time = dos.get_blocked_time()

    calendar_settings = models.CalendarSettings.GetCalendarSettings()
    cf_settings = CustomFormSettings.GetSettings(request=request)
    curr_session_type_choices = None
    try:
        curr_session_type_choices = dos.session_type
    except AttributeError:
        pass
    render_to_response_dict = {
        'session_type_choices': cf_settings.get_session_type_choices(),
        'curr_session_type_choices': curr_session_type_choices,
        "calendar_links": calendar_links,
        "dos_form": form,
        "submit_link": submit_link,
        "links": links,
        "year": year,
        # quirk because fullcalendar js expects 0 based month
        "month": int(month) - 1,
        "day": day,
        "displayweekends":
        models.CalendarSettings.GetDisplayWeekend(calendar_settings),
        "calendar_start_time":
        '%02d:00:00' % int(models.CalendarSettings.GetStartTime(calendar_settings)),
        "blocked_time": blocked_time,
    }
    if invoice is not None:
        view_common.add_popup(render_to_response_dict, invoice)
    return render_to_response(
        "calendar_template.html",
        render_to_response_dict, context_instance=RequestContext(request)
    )


def calendar_feed(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    if not start:
        logging.info('[calendar_feed] start was not set')
        return HttpResponse('')
    if not end:
        logging.info('[calendar_feed] end was not set')
        return HttpResponse('')
    starttime = datetime.datetime.combine(
        datetime.datetime.strptime(start, '%Y-%m-%d').date(),
        datetime.time.min)
    endtime = datetime.datetime.combine(
        datetime.datetime.strptime(end, '%Y-%m-%d').date(),
        datetime.time.max)
    cal_feed = CalendarFeed(request, starttime,
                            endtime)
    return HttpResponse(cal_feed.GetFeed(), mimetype='application/json')


def calendar_update_dos(request, dos_id, year, month, day):
    dos = models.DOS.safe_get_by_id(int(dos_id), request)
    if not dos:
        view_common.log_access_violation('calendar_update_dos')
        # TODO: show an error message
        return HttpResponseRedirect(reverse('calendar'))
    if year and month and day:
        request_date = datetime.datetime(int(year), int(month), int(day))
    else:
        request_date = datetime.datetime.today()
        calendar_links = CalendarLinks(request_date)
        logging.error('in calendar_update_dos but year, month and/or day was'
                      ' invalid (%s, %s, %s, %s)', dos_id, year, month, day)
        return HttpResponseRedirect(calendar_links.get_absolute_url())
    calendar_links = CalendarLinks(request_date)

    if request.method == 'POST':
        form = models.DOSForm(request.POST, request=request)
        if form.is_valid():
            form_dict = form.cleaned_data
            try:
                client = models.ClientInfo.safe_get_by_id(
                    int(form.cleaned_data['clientinfo']), request=request)
                form_dict['clientinfo'] = client
            except ValueError:  # catches calling int on non integer
                form_dict['clientinfo'] = None
            dos.update_model(form_dict)
            dos = view_common.save_entity(request, dos)
            print_receipt = form.cleaned_data.get('print_receipt')
            if print_receipt:
                return HttpResponseRedirect(
                    calendar_links.get_receipt_absolute_url(int(dos.get_id())))
        else:
            logging.error('in calendar_update_dos and form was invalid.'
                          ' POST: %s.' % (request.POST))
            logging.error(''.join(['%s %s' % (field.label, field.errors)
                                   for field in form if field.errors]))
    else:
        logging.error('in calendar_update_dos and method was not POST')
    return HttpResponseRedirect(calendar_links.get_absolute_url())


def calendar_delete_dos(request, dos_id, year, month, day):
    dos = models.DOS.safe_get_by_id(int(dos_id), request)
    if not dos:
        view_common.log_access_violation('calendar_delete_dos')
        # TODO: show an error message
        return HttpResponseRedirect(reverse('calendar'))
    dos.delete()
    if year and month and day:
        request_date = datetime.datetime(int(year), int(month), int(day))
    else:
        request_date = datetime.datetime.today()
    calendar_links = CalendarLinks(request_date)
    return HttpResponseRedirect(calendar_links.get_absolute_url())


def calendar_cancel_all_series_dos(request, dos_id, year, month, day):
    dos = models.DOS.safe_get_by_id(int(dos_id), request)
    if not dos:
        view_common.log_access_violation('calendar_cancel_all_series_dos')
        # TODO: show an error message
        return HttpResponseRedirect(reverse('calendar'))
    if year and month and day:
        request_date = datetime.datetime(int(year), int(month), int(day))
    else:
        request_date = datetime.datetime.today()
    calendar_links = CalendarLinks(request_date)
    dos.dos_repeat = 'No'
    dos.save()
    return HttpResponseRedirect(calendar_links.get_absolute_url())
