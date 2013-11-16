import re
from django import forms
from django.forms.widgets import DateInput
from django.forms.widgets import Select
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe


# Attempt to match many time formats:
# Example: "12:34:56 P.M."  matches:
# ('12', '34', ':56', '56', 'P.M.', 'P', '.', 'M', '.')
# ('12', '34', ':56', '56', 'P.M.')
# Note that the colon ":" before seconds is optional, but only if seconds are
# omitted
time_pattern = (r'(\d\d?):(\d\d)(:(\d\d))?'
                ' *((a{1}|A{1}|p{1}|P{1})(\.)?(m{1}|M{1})(\.)?)?$')

RE_TIME = re.compile(time_pattern)
# The following are just more readable ways to access re.matched groups:
HOURS = 0
MINUTES = 1
SECONDS = 3
MERIDIEM = 4


class SelectTimeWidget(Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>,
    or as 12hr: <hour>:<minute>:<second> <am|pm>

    Also allows user-defined increments for minutes/seconds
    """
    field_name = '%s_time'

    def __init__(self, attrs=None, minute_step=None):
        '''
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format
        (rather than 24-hr)
        '''
        self.attrs = attrs or {}

        self.hours = range(0, 12)
        self.hours[0] = 12

        if minute_step:
            self.minutes = range(0, 60, minute_step)
        else:
            self.minutes = range(0, 60)

        super(SelectTimeWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        # hour_val, minute_val, second_val = value.hour, value.minute,
        # value.second
        if isinstance(value, str) or isinstance(value, unicode):
            (h, left_over) = value.split(':')
            try:
                (m, unused_meridiem) = left_over.split(' ')
            except ValueError:
                m = left_over
                hour_val = int(h)
                minute_val = int(m)
            hour_val = int(h)
            minute_val = int(m)
        elif value is None:
            hour_val = 0
            minute_val = 0

        else:
            hour_val, minute_val = value.hour, value.minute
        if hour_val >= 12:
            self.meridiem_val = 'pm'
        else:
            self.meridiem_val = 'am'

        if hour_val >= 13:
            hour_val -= 12

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # NOTE: for times to get displayed correctly, the values MUST be
        # converted to unicode  When Select builds a list of options, it
        # checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        #second_val = u"%.2d" % second_val

        hour_choices = ["%.2d" % i for i in self.hours]
        local_attrs = self.build_attrs(id=self.field_name % id_)
        minute_choices = ["%.2d" % i for i in self.minutes]
        meridiem_choices = ["am", "pm"]
        choices = [('%s:%s %s' % (hour, minute, meridiem),
                    '%s:%s %s' % (hour, minute, meridiem))
                    for meridiem in meridiem_choices
                    for hour in hour_choices
                    for minute in minute_choices]

        select_html = Select(choices=choices).render(
            self.field_name % name,
            '%s:%s %s' % (hour_val, minute_val, self.meridiem_val),
            local_attrs)
        output = []
        output.append(select_html)
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return self.field_name % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        time = data.get(self.field_name % name, None)
        if time:
            (h, left_over) = time.split(':')
            (m, meridiem) = left_over.split(' ')

            #NOTE: if meridiem IS None, assume 24-hr
            if meridiem is not None:
                if meridiem.lower().startswith('p') and int(h) != 12:
                    h = (int(h) + 12) % 24
                elif meridiem.lower().startswith('a') and int(h) == 12:
                    h = 0
            return '%02d:%02d' % (int(h), int(m))
        #if (int(h) == 0 or h) and m:
        #    return '%s:%s' % (h, m)
        return None


class SplitSelectDateTimeWidget(forms.MultiWidget):
    '''
    This class combines SelectTimeWidget
    (from: http://www.djangosnippets.org/snippets/1202/)
    and SelectDateWidget (from django.forms.extras) so we have something
    like SpliteDateTimeWidget (in django.forms.widgets), but with Select
    elements.
    '''
    def __init__(self, attrs=None, minute_step=None, years=None):
#        ''' pass all these parameters to their
#            respective widget constructors...
#        '''
        widgets = (DateInput(attrs=attrs),
                   SelectTimeWidget(attrs=attrs, minute_step=minute_step))
        super(SplitSelectDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value.time().replace(microsecond=0)
            value.time().replace(second=0)

            return [value.date(), value.time()]
        return [None, None]

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        rendered_widgets.insert(-1,
                                '</td></tr><tr><th><label></label></th><td>')
        return u''.join(rendered_widgets)
