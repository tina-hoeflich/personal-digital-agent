import pytest
from app import app  # Flask instance of the API


def test_index_route():
	response = app.test_client().get('/')

	assert response.status_code == 404


def test_input_route():
	test_input = "Hello from api test example."
	response = app.test_client().post('/input', data=test_input)

	assert response.status_code == 200
	assert test_input in response.text
