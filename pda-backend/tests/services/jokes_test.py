import pytest
from unittest.mock import patch

import services.jokes as jokes_service


@pytest.mark.asyncio
@patch("jokeapi.main.Joke_Class.get_joke", return_value={"type": "single", "joke": "I am funny!"})
async def test_single_joke(joke_mock):
	joke = await jokes_service.get_joke()
	assert "I am funny!" in joke
	joke_mock.assert_called_once()


@pytest.mark.asyncio
@patch("jokeapi.main.Joke_Class.get_joke", return_value={"type": "twopart", "setup": "Why am I funny?", "delivery": "Because I am!"})
async def test_joke_question(joke_mock):
	joke = await jokes_service.get_joke()
	assert "Why am I funny? Because I am!" in joke
	joke_mock.assert_called_once()
