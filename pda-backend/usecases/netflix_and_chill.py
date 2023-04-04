import icalendar
from tmdbv3api import TMDb, Movie
from datetime import datetime, date
from justwatch import JustWatch

tmdb = TMDb()
tmdb.api_key = 'b3e56fddd812de48269710ffd2f749e4'
tmdb.language = 'en'
tmdb.debug = True

just_watch = JustWatch(country='DE')

movie = Movie()
popular = movie.popular()

# for p in popular:
#     print(p.id)
#     print(p.title)
#     print(p.overview)
#     print(p.poster_path)

results = just_watch.search_for_item(query='frozen', provider=['netflix'], content_types=['movie'])

results = results['items']
if len(results) > 0:
    title = results[0]['title']
    netflix_available = any(provider['provider_id'] == 8 for provider in results[0]['offers'])
    if netflix_available:
        print(f"{title} is available on Netflix!")
    else:
        print(f"{title} is not available on Netflix.")
else:
    print("No results found.")



# Get today's date
today = date.today()

# Open the iCalendar file
with open(r'pda-backend\resources\student_calender.ics', 'rb') as f:
    calendar = icalendar.Calendar.from_ical(f.read())

# Iterate over each event in the calendar
for component in calendar.walk():
    if component.name == "VEVENT":
        event = {}
        # Extract the event information
        event["summary"] = str(component.get('summary'))
        event["location"] = str(component.get('location'))
        event["description"] = str(component.get('description'))
        event["start_time"] = component.get('dtstart').dt
        event["end_time"] = component.get('dtend').dt

        # Check if the event occurs today
        if event["start_time"].date() == today or event["end_time"].date() == today:

            # Print the event information
            print("Event: " + event["summary"])
            print("Location: " + event["location"])
            print("Description: " + event["description"])
            print("Start Time: " + str(event["start_time"]))
            print("End Time: " + str(event["end_time"]))