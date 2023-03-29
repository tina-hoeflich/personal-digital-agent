from jokeapi import Jokes 

async def print_joke():
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke(blacklist=["nsfw", "religious", "political", "racist", "sexist"])  # Retrieve a random joke without nsfw, religious, political, racist, sexist jokes
    if joke["type"] == "single": # Print the joke
        text = joke["joke"]
    else:
        # print(joke["setup"])
        # print(joke["delivery"])
        text = joke["setup"] + " " + joke["delivery"]
    return text

