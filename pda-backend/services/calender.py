import icalendar
from datetime import datetime, date, timedelta

def get_last_event() -> tuple[str, datetime.time, datetime.time]:
    """This method gets the last event of the day from the student calender.

    Returns:
        tuple[str, datetime.time, datetime.time]: name of last event, end time of last event, time to watch movie
    """    
    date_today = date.today()

    with open(r'resources\student_calender.ics', 'rb') as f:
        calendar = icalendar.Calendar.from_ical(f.read())

    last_event_end_time = None

    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {}
            event["summary"] = str(component.get('summary'))
            event["start_time"] = component.get('dtstart').dt
            event["end_time"] = component.get('dtend').dt

            if event["start_time"].date() == date_today or event["end_time"].date() == date_today:
                if last_event_end_time is None or event["end_time"].time() > last_event_end_time.time():
                    last_event_end_time = event["end_time"]
                    last_event_name = event["summary"]
    
    if last_event_end_time is not None:
        last_event_end_time = last_event_end_time.time()
        new_time = (datetime.combine(date_today, last_event_end_time) + timedelta(hours=1, minutes=30)).time()
        return last_event_name, last_event_end_time, new_time
    else:
        return None, None, None
    
from datetime import date, datetime, timedelta
import icalendar

def get_first_event_start_time() -> tuple[str, datetime.time]:
    """This method gets the start time of the first event of the day from the student calendar.

    Returns:
        tuple[str, str, datetime.time]: name of first event, start time of first event
    """
    date_today = date.today()

    with open(r'resources\student_calender.ics', 'rb') as f:
        calendar = icalendar.Calendar.from_ical(f.read())

    first_event_start_time = None

    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {}
            event["summary"] = str(component.get('summary'))
            event["start_time"] = component.get('dtstart').dt
            event["end_time"] = component.get('dtend').dt

            if event["start_time"].date() == date_today:
                if first_event_start_time is None or event["start_time"].time() < first_event_start_time.time():
                    first_event_start_time = event["start_time"]
                    first_event_name = event["summary"]

    if first_event_start_time is not None:
        return first_event_name, first_event_start_time.time()
    else:
        return None, None
