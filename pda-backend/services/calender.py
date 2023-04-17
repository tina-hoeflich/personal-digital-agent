import icalendar
from datetime import datetime, date, timedelta

def get_last_event():
    # Get today's date
    today = date.today()

    # Open the iCalendar file
    with open(r'resources\student_calender.ics', 'rb') as f:
        calendar = icalendar.Calendar.from_ical(f.read())

    # Initialize a variable to store the last event's end time
    last_event_end_time = None

    # Iterate over each event in the calendar
    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {}
            # Extract the event information
            event["summary"] = str(component.get('summary'))
            event["start_time"] = component.get('dtstart').dt
            event["end_time"] = component.get('dtend').dt

            # Check if the event occurs today
            if event["start_time"].date() == today or event["end_time"].date() == today:
                # Update the last event's end time if it's later than the current value
                if last_event_end_time is None or event["end_time"].time() > last_event_end_time.time():
                    last_event_end_time = event["end_time"]
                    last_event_name = event["summary"]

    # Check if there was at least one event occurring today
    if last_event_end_time is not None:
        # Extract the time from the datetime object
        last_event_end_time = last_event_end_time.time()

        # Add one and a half hours to the last event's end time
        new_time = (datetime.combine(today, last_event_end_time) + timedelta(hours=1, minutes=30)).time()

        # return the name and the time of the updated end time
        return last_event_name, last_event_end_time, new_time
    else:
        return "No events today.",None, None