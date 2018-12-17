from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class InterviewCalendar(HTMLCalendar):

    def __init__(self, interviews):
        super(InterviewCalendar, self).__init__()
        self.interviews = self.group_by_day(interviews)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' '
            if day in self.interviews:
                cssclass += ' h4'
                body = []
                for interview in self.interviews[day]:
                    body.append('<a href="/allInterview/onDate/%s/%s/%s">' % (self.year, self.month, day))
                    #body.append(esc(str(interview)))
                    body.append('%s</a>' % day)

                return self.day_cell(cssclass, '%s' % ''.join(body))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month, withyear=True):
        year = int(year)
        month = int(month)
        self.year, self.month = int(year), int(month)
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table table-bordered">')
        a('\n')
        a(self.formatmonthname(year, month, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(year, month):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def group_by_day(self, interviews):
        field = lambda interview: interview.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(interviews, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
