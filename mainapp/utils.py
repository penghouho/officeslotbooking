from calendar import HTMLCalendar
from .models import Booking
from django.utils.safestring import mark_safe
from datetime import date


class BookingCalendar(HTMLCalendar):
    def __init__(self, bookings=None):
        super(BookingCalendar, self).__init__()
        self.bookings = bookings

    def formatday(self, day, weekday, bookings, theyear, themonth):
        """
        Return a day as a table cell.
        """

        if day == 0: #empty cells
          return '<td class="noday">&nbsp;</td>'

        bookings_from_day = bookings.filter(book_date__day=day).count()
        target_date = str(theyear) + '-' + str(themonth) + '-' + str(day)

        if bookings_from_day is 0:
          bookings_html = '<br />'
        elif bookings_from_day is 19: # TODO replace by setting value - 1
          bookings_html = '<h2 class="text-warning">' + '<br />' + str(bookings_from_day) + '</h2>'
        elif bookings_from_day is 20: # TODO replace by setting value
          bookings_html = '<h2 class="text-danger">' + '<br />' + str(bookings_from_day) + '</h2>'
        else:
          bookings_html = '<h2>' + '<br />' + str(bookings_from_day) + '</h2>'

        if date(year=2021, month=10, day=3) < date(year=theyear, month=themonth, day=day):
          bookings_html += '<a href="/date_details?date=%s">Details</a>' % target_date
        return '<td class="align-top %s">%d%s</td>' % (self.cssclasses[weekday], day, mark_safe(bookings_html))

    def formatweek(self, theweek, bookings, theyear, themonth):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, bookings, theyear, themonth) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        bookings = Booking.objects.filter(book_date__month=themonth)

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, bookings, theyear, themonth))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)