from django.conf.urls import url
from django.contrib.auth.models import User, Group
from .models import Booking
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer, BookingSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from datetime import datetime
from django.utils.safestring import mark_safe
from .utils import BookingCalendar
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.contrib import messages

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

def index(request):
    if request.user.is_authenticated:
        queryprms = request.GET
        month_string = queryprms.get('month')
        year_string = queryprms.get('year')

        month = int(month_string) if month_string is not None and month_string.isdigit() else None
        year = int(year_string) if year_string is not None and year_string.isdigit() else None

        today = datetime.today()
        current_month = today.month
        current_year = today.year
        if year is None:
            year = current_year
        if month is None:
            month = current_month

        html_calendar = BookingCalendar()
        cal = html_calendar.formatmonth(year, month, withyear=True)
        cal = cal.replace('<td ', '<td width="150" height="150"')
        cal = mark_safe(cal)

        if month == 1:
            previous_month = 12
            previous_year = year - 1
        else:
            previous_month = month - 1
            previous_year = year

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        """View function for home page of site."""
        context = {
            'month': month,
            'year': year,
            'next_month_url': '?month=' + str(next_month) + '&year=' + str(next_year),
            'current_month_url': '?month=' + str(current_month) + '&year=' + str(current_year),
            'previous_month_url': '?month=' + str(previous_month) + '&year=' + str(previous_year),
            'num_instances_available': 3,
            'num_authors': 4,
            'cal': cal
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'index.html', context=context)
    else:
        return redirect('accounts/login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def date_details(request):
    if request.user.is_authenticated:
        queryprms = request.GET
        date_string = queryprms.get('date')
        try:
            target_date = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            target_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        bookings_from_day = Booking.objects.filter(book_date=target_date)
        is_joined = bookings_from_day.filter(user=request.user).exists()
        bookings_count = bookings_from_day.count()
        context = {
            'bookings_from_day': enumerate(bookings_from_day,start= 1),
            'date': target_date.strftime("%Y-%m-%d"),
            'is_joined': is_joined,
            'reached_limit': bookings_count >= 20,
            'bookings_count': bookings_count,
        }
        print(context)
        return render(request, 'date_details.html', context=context)
    else:
        return redirect('accounts/login')


@require_http_methods(["POST"])
def create_booking(request):
    if request.user.is_authenticated:
        date_string = request.POST.get('date')
        try:
            target_date = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            target_date = None
        if target_date is None or target_date <= datetime.strptime('2021-10-03', "%Y-%m-%d"):
            return HttpResponseRedirect('/')
        else:
            bookings_count = Booking.objects.filter(book_date=target_date).count()
            if bookings_count < 20:
                booking = Booking(book_date=target_date, user=request.user)
                try:
                    booking.save()
                except Exception as e:
                    print(e)
            return HttpResponseRedirect('/date_details/?date=%s' % request.POST.get('date'))
    else:
        return HttpResponseRedirect('accounts/login')


@require_http_methods(["POST"])
def delete_booking(request):
    if request.user.is_authenticated:
        date_string = request.POST.get('date')
        try:
            target_date = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            target_date = None
        if target_date is None:
            return HttpResponseRedirect('/')
        else:
            booking = Booking.objects.filter(book_date=target_date).filter(user=request.user).first()
            try:
                booking.delete()
            except Exception as e:
                print(e)
            return HttpResponseRedirect('/date_details/?date=%s' % request.POST.get('date'))
    else:
        return HttpResponseRedirect('accounts/login')