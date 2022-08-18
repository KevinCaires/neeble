"""
Bot commands.
"""
import logging
from random import choice

from discord.ext import commands

from utils.database import get_by_id, get_quotes, remove_quote, set_quote, count_quotes

client = commands.Bot(command_prefix='--')
logger = logging.getLogger(__name__)

quote_id_stack = []

@client.command(aliases=['q'])
async def quote(bot: object, *quote: str) -> str:
    """
    Save a quote into database.
    """
    if not quote:
        return await bot.send('You\'re not my mute uncle, tell me something to remember.\n(You have\'nt provided a quote')

    quote = ' '.join(quote)

    if 'http' in quote and 'discord' in quote and not quote[-4:] == '.png':
        return await bot.send("- _Check your link, dumbass! You're trying to quote an image from a message, but you're quoting the message itself!_\n"\
            "(Make sure to copy the link for the image by clicking on it, right-clicking the image and then clicking on \"Save Link\"")

    try:
        user = bot.author.name
        set_quote(user, quote)
    except Exception as ex:
        return await bot.send(f'{ex.args}\n_What the fuck are you doing?_')
    else:
        return await bot.send('Done:\n`%s`' % quote)


@client.command(aliases=['rq'])
async def random_quote(bot: object) -> str:
    """
    Get an random quote from database.
    """
    quotes = get_quotes(quote_id_stack)
    stack_limit = int((len(quotes) * .25))
    stack_len = len(quote_id_stack)

    if not quotes and stack_len > 0:
        quote_id_stack.pop(0)
        quotes = get_quotes(quote_id_stack)
    elif not quotes:
        return await bot.send('You\'ve got no quotes saved yet.\n(Save quotes by using `--q <quote`')

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
async def by_id(bot, _id: int=None) -> str:
    """
    Get quote by ID.
    """
    syntax = "`--qid <quote id>`"
    
    if not _id:
        return await bot.send("_If you don't tell me the ID, how the fuck do you expect me to quote it to you!?_\n(The correct syntax is " + syntax )

    if not isinstance(_id, int):
        return await bot.send("_Don't fuck with me, you asshole. The ID needs to be an interger!_\n(The correct syntax is " + syntax)

    quote = get_by_id(_id)

    if not quote:
        return await bot.send("_Wrong ID, sucker!_\n(There's no such quote with id " + _id)

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
    Delete one quote by database ID.
    """
    syntax = "`--dq <quote id>`"
    roles = [r.name for r in bot.author.roles]

    if not 'Operador' in roles:
        return await bot.send("_And who the fuck do **YOU** think you are!?_.\n"\
            "(You don't have the necessary role for this command")
    
    if not _id:
        return await bot.send("_If you don't tell me the ID, how the fuck do you expect me to delete it to you!?_\n(The correct syntax is " + syntax )

    if not isinstance(_id, int):
        return await bot.send("_Don't fuck with me, you asshole. The ID needs to be an interger!_\n(The correct syntax is " + syntax)

    quote = get_by_id(_id)

    if not quote:
        return await bot.send("_Wrong ID, sucker!_\n(There's no such quote with id " + _id)

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

@client.command(aliases=['cq', 'cquotes'])
async def quote_count(bot: object) -> str:
    """
    Outputs a quote count from the database
    """

    # For len(amount) to work, first it needs to be converted into str
    amount = count_quotes()
    amount = str(amount)
    amount = amount[1:len(amount)][:-2]

    msg = "Quote count: `" + amount + "`"

    return await bot.send(msg)