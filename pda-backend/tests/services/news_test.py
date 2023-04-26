import services.news as news

mock_stories = [{"title": "STORY TITLE", "description": "STORY DESCRIPTION"}] * 10

news.news_cache = {
    "results": mock_stories
}

def test_news_title():
    text = news.get_news_title()
    assert text == "STORY TITLE"

def test_news_content():
    text = news.get_news_content()
    assert text == "STORY DESCRIPTION"