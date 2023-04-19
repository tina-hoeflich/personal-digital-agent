from jokeapi import Jokes


async def get_joke():
    """
    Method that retrieves a random joke from the jokeapi
    :return: the joke
    """
    j = await Jokes()
    joke = await j.get_joke(blacklist=["nsfw", "religious", "political", "racist", "sexist"])  # Retrieve a random joke without nsfw, religious, political, racist, sexist jokes
    if joke["type"] == "single":
        text = joke["joke"]
    else:
        text = joke["setup"] + " " + joke["delivery"]
    return text

