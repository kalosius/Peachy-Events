from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from . models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Import Pagination Stuff
from django.core.paginator import Paginator



# Admin approval page
def admin_approval(request):

    # Get The Venues
    venue_list = Venue.objects.all()


    # Get Counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            # Uncheck All Events
            event_list.update(approved=False)
            # Update the Database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, "Event List Approval Has Been Updated!")
            return redirect('list-events')
        else:
            return render(request, 'events/admin_approval.html', {'event_list':event_list, 'event_count':event_count, 'venue_count':venue_count, 'user_count':user_count, 'venue_list':venue_list})
    else:
        messages.success(request, "You Aren't Authorized To View This Page")
        return redirect('home')


# Create My Events Page
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {"events":events})
    else:
        messages.success(request, "You aren't Authorized To View This Page")
        return redirect('home')




# Generate PDF files for venues
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text Object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    # Designate the Model
    venues = Venue.objects.all()
    # Create a blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venues.pdf')
    
# Generate Text File Venue List
def venue_csv(request):
    response  = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    # Creaate a CSv writer
    writer = csv.writer(response)

    # Designate the Model
    venues = Venue.objects.all()

    # Add colunm headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])
   
    # Loop through  and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    return response

# Generate Text File Venue List
def venue_text(request):
    response  = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate the Model
    venues = Venue.objects.all()
    # Create a blank list
    lines = []
    # Loop through  and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.email_address}\n{venue.web}')
    # Manual lines
    # lines = ["Thhis is something\n", "This is Line Two\n", "This is line 3\n"]
    response.writelines(lines)
    return response


# Delete an venue
def delete_venue(request, venue_id):
    venue  = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


# Delete an event
def delete_event(request, event_id):
    event  = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event Deleted!')

        return redirect('list-events')
    else:
        messages.success(request, "You aren't Authorized To Delete This Event!")
        return redirect('list-events')


def update_event(request, event_id):
    event  = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {'event':event, 'form':form})


def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form =EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True') 
        else:
            form =EventForm(request.POST) 
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user #Logged in user  
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just Going to the page, Not submitting
        if request.user.is_superuser:
            form =EventFormAdmin(request.POST)
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'venue':venue, 'form':form})


def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched':searched, 'venues':venues})
    else:
        return render(request, 'events/search_venues.html', {})


def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)
        return render(request, 'events/search_events.html', {'searched':searched, 'events':events})
    else:
        return render(request, 'events/search_events.html', {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {'venue':venue, 'venue_owner':venue_owner})


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('name')
    # venue_list = Venue.objects.all().order_by('?')  #this orders randomly
    venue_list = Venue.objects.all()

    # Setup Pagination
    p = Paginator(Venue.objects.all().order_by('-id'), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    
    return render(request, 'events/venues.html', {'venue_list':venue_list, 'venues':venues, 'nums':nums})


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id #Logged in user  
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('name')
    return render(request, 'events/event_list.html', {'event_list':event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = request.user
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create Calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year

    # Query the events Model For Dates
    event_list = Event.objects.filter(event_date__year = year, event_date__month = month_number)

    # Get current Time
    time = now.strftime('%I:%M %p')
    return render(request, 'events/home.html', {'name':name, 'year':year, 'month':month, 'month_number':month_number, 'cal':cal, 'current_year':current_year, 'time':time, 'event_list':event_list})

