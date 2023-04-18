import services.calender as calender

def test_get_last_event(): 
    last_event_name, last_event_end_time, new_time = calender.get_last_event()
    
    assert type(last_event_name) == str or last_event_name == None
    assert type(last_event_end_time) == str or last_event_end_time == None
    assert type(new_time) == str or new_time == None