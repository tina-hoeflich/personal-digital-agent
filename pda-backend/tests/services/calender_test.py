import services.calender as calender
from datetime import datetime, time

def test_get_last_event(): 
    last_event_name, last_event_end_time, new_time = calender.get_last_event()
    
    assert type(last_event_name) == str or last_event_name == None
    assert isinstance(last_event_end_time, time) or last_event_end_time == None
    assert isinstance(new_time, time) or new_time == None

def test_get_first_event_start_time(): 
    first_event_name, first_event_start_time = calender.get_first_event_start_time()
    
    assert type(first_event_name) == str or first_event_name == None
    assert isinstance(first_event_start_time, datetime) or first_event_start_time == None