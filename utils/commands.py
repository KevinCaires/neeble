"""
Bot commands.
"""
import logging
from random import choice

from discord.ext import commands
from discord import Intents, Embed
from settings.config import IMAGE_TYPES, PERMISSIONS

from utils.database import get_by_id, get_quotes, remove_quote, set_quote, count_quotes
from utils.weather import geocode, getweatherdata, displayweather

from settings.config import PERMISSIONS, OW_API_CONFIG
from utils.database import (count_quotes, get_by_id, get_quote_contains,
                            get_quotes, remove_quote, set_quote)

client = commands.Bot(command_prefix='--', intents=Intents.all())
logger = logging.getLogger(__name__)

quote_id_stack = []


@client.command(aliases=['q'])
async def quote(bot: object, *quote: str) -> str:
    """
    Saves a quote into the database.
    """
    if not quote:
        return await bot.send('You\'re not my mute uncle, tell me something to remember.\n'\
            '(You haven\'t provided a quote)')

    quote = ' '.join(quote)

    if 'http' in quote and 'discord' in quote and not quote[-4:] in IMAGE_TYPES:
        return await bot.send("- _Check your link, dumbass! You're trying to quote an image from a"\
            " 'message, but you're quoting the message itself!_\n"\
            "'(Make sure to copy the link for the image by clicking on it, right-clicking the "\
            "image and then clicking on \"Save Link\")'")

    try:
        user = bot.author.name
        qtid = set_quote(user, quote)
    except Exception as ex:
        if ex.args[0].find("Duplicate") != -1:
            return await bot.send("There's already a quote from that same person, with that "\
                "exact match!")
        return await bot.send(f'{ex.args}\n_What the fuck are you doing?_')
    else:
        return await bot.send(f"Done: `{quote}\n` ID: `{qtid}`")


@client.command(aliases=['rq'])
async def random_quote(bot: object) -> str:
    """
    Get a random quote from the database.
    """
    quotes = get_quotes(quote_id_stack)
    stack_limit = int((len(quotes) * .25))
    stack_len = len(quote_id_stack)

    if not quotes and stack_len > 0:
        quote_id_stack.pop(0)
        quotes = get_quotes(quote_id_stack)
    elif not quotes:
        return await bot.send('You\'ve got no quotes saved yet.\n(Save quotes by using '\
            '`--q <quote`)')

    chosen_one = choice(quotes)
    quote_id_stack.append(chosen_one.id)

    if stack_len >= stack_limit:
        quote_id_stack.pop(0)

    try:
        # To image links.
        if 'http' in chosen_one.quote:
            return await bot.send(f'{chosen_one.quote}')
        return await bot.send(f'{chosen_one.quote}\n`By: {chosen_one.user}`')

    except Exception as ex:
        return await bot.send(ex)


@client.command(aliases=['qid'])
async def by_id(bot: object, _id: int=None) -> str:
    """
    Gets one quote by ID.
    """
    syntax = "`--qid <quote id>`"
    
    if not _id:
        return await bot.send("_If you don't tell me the ID, how the fuck do you expect me to "\
            f"quote it to you!?_\n(The correct syntax is {syntax})")

    quote = get_by_id(_id)

    if not quote:
        return await bot.send(f"_Wrong ID, sucker!_\n(There's no such quote with id {_id})")

    try:
        # To image links.
        if 'http' in quote.quote:
            return await bot.send(f'{quote.quote}')
        return await bot.send(f'{quote.quote}\n`By: {quote.user}`')

    except Exception as ex:
        return await bot.send(ex)


@client.command(aliases=['dq'])
async def delete_quote(bot, _id: int=None) -> str:
    """
    Deletes one quote by ID.
    """
    syntax = "`--dq <quote id>`"
    roles = [r.name for r in bot.author.roles]
    PermStatus = False

    if len(PERMISSIONS['dq']) < 1 or not len(set(PERMISSIONS['dq']).intersection(roles)) < 1:
        PermStatus = True

    if not PermStatus:
        return await bot.send("_And who the fuck do **YOU** think you are!?_.\n"\
            "(You don't have the necessary role for this command)")

    if not _id:
        return await bot.send("_If you don't tell me the ID, how the fuck do you expect me to "\
            f"delete it to you!?_\n(The correct syntax is {syntax})")

    quote = get_by_id(_id)

    if not quote:
        return await bot.send(f"_Wrong ID, sucker!_\n(There's no such quote with id {_id})")

    try:
        if not remove_quote(_id):
            return await bot.send('_Something wrong happened, dude!_')
        return await bot.send('_Evidence deleted, fella!_')

    except Exception as ex:
        return await bot.send(ex)


@client.command(aliases=['qstack'])
async def queue_stack(bot: object) -> str:
    """
    Displays the 5 quote history stack
    """
    return await bot.send('A list of the 5 latest message IDs follows:'\
        f' `{",".join(str(q) for q in quote_id_stack[-5:])}`')

@client.command(aliases=['qc', 'cquotes'])
async def quote_count(bot: object) -> str:
    """
    Outputs a quote count from the database
    """
    amount = count_quotes()
    msg = f"Quote count: `{amount}`"

    return await bot.send(msg)


@client.command(aliases=['v', 'version'])
async def info(bot: object) -> str:
    """
    Displays the bot's information
    """
    roles = [r.name for r in bot.author.roles]
    PermStatus = False

    if len(PERMISSIONS['v']) < 1 or not len(set(PERMISSIONS['v']).intersection(roles)) < 1:
        PermStatus = True

    if not PermStatus:
        return await bot.send("_And who the fuck do **YOU** think you are!?_.\n"\
            "(You don't have the necessary role for this command)")
    
    motd = open("./motd", mode='r')
    text = motd.readlines()
    fullbanner = ""

    for lines in text:
        fullbanner = fullbanner + lines
    msg = f'''```\n{fullbanner}\n```'''

    return await bot.send(msg)


@client.command(aliases=['w'])
async def weather(bot: object, *location: str) -> str:
    """
    Displays the weather information for a given place
    """
    if OW_API_CONFIG['api_id'] == 'no':
        return await bot.send("You haven't set up an API key! Make an user and set up an API key in https://openweathermap.org/\n \
        (The weather command hansn't been set up properly, make sure you have `OPENWEATHER_API_TOKEN` set up")
    if location:
        location = str(location)
        stripped = location.replace(" ", "") # Strips all whitespace
        separated = stripped.split(',') # Splits between commas
        separated.pop(-1)
        separated[0] = separated[0][1:len(separated[0])]  # These two commands clean up input for the parser
        
        if len(separated) > 3:
            return await bot.send("This command takes 3 parameters at most!\n \
            (Syntax: `--w <city>, <state>, <ISO 3166 country code>`)")
        if len(separated) == 1:
            city = separated[0]
            state = ""
            country = ""
        elif len(separated) == 2:
            city = separated[0]
            state = separated[1]
            country = ""
        else:
            city = separated[0]
            state = separated[1]
            country = separated[2]        
    else:
        city = ""
        state = ""
        country = ""
    
    lat, lon = geocode(city, state, country)
    weatherdata = getweatherdata(lat, lon)
    msg = displayweather(weatherdata)
    default_msg = 'No data!'
    embed = Embed(type='rich')
    embed.add_field(
        name='City',
        value=msg.name,
    )
    embed.add_field(
        name='Description',
        value=msg.description if msg.description else default_msg,
    )
    embed.add_field(
        name='Temperature ºC',
        value=msg.temp if msg.temp else default_msg,
    )
    embed.add_field(
        name='Feels like ºC',
        value=msg.feels_like if msg.feels_like else default_msg,
    )
    embed.add_field(
        name='Humidity %',
        value=msg.humidity if msg.humidity else default_msg,
    )
    embed.add_field(
        name='Cloud coverage %',
        value=msg.cloud_coverage if msg.cloud_coverage else default_msg,
    )
    embed.add_field(
        name='Wind gusts m/s',
        value=msg.wind_gusts if msg.wind_gusts else default_msg,
    )
    embed.add_field(
        name='Wind speed m/s',
        value=msg.wind_speed if msg.wind_speed else default_msg,
    )

    return await bot.send('**`Weather`**', embed=embed)


@client.command(aliases=['qcontains', 'qsearch'])
async def quote_contains(bot: object, part: str) -> str:
    """
    Filter quote by part of saved message.
    """
    syntax = '--qcontains <part>'

    if not part:
        return await bot.send("_If you don't tell me the part, how the fuck do you expect me to "\
            f"find it to you!?_\n(The correct syntax is {syntax})")

    quotes = get_quote_contains(part)

    if not quotes:
        return await bot.send(f"_Wrong text, sucker!_\n(There's no such quote with text `{part}`)")

    for quote in quotes:
        await bot.send(f'```\nID: {quote.id}\nMessage: {quote.quote[:10]} ... '\
            f'{quote.quote[-10:]}\nUser: {quote.user}\n```')

    return
