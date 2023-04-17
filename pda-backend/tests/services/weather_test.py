import services.weather as weather

lat, lng = (48.777, 9.177)

def test_weather_code():
    code = weather.get_weather_code(lat, lng)
    assert code >= 200
    assert code <= 804

def test_weather_city():
    _, city, _ = weather.get_current_weather(lat, lng)
    assert city == "Stuttgart"

def test_weather_temps():
    min_temp, max_temp, _ = weather.get_weather_forecast(lat, lng)
    assert min_temp <= max_temp