from calendar import HTMLCalendar
from .models import Booking


class BookingCalendar(HTMLCalendar):
    def __init__(self, bookings=None):
        super(BookingCalendar, self).__init__()
        self.bookings = bookings

    def formatday(self, day, weekday, bookings):
        """
        Return a day as a table cell.
        """
        bookings_from_day = bookings.filter(book_date__day=day).count()

        if bookings_from_day is 0:
          bookings_html = ''
        else:
          bookings_html = '<h1>' + '<br />' + str(bookings_from_day) + '</h1>'
          return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, bookings_html)

        if day == 0:
          return '<td class="noday">&nbsp;</td>'
        else:
          return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, bookings_html)

    def formatweek(self, theweek, bookings):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, bookings) for (d, wd) in theweek)
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
            a(self.formatweek(week, bookings))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)