"""
Bot commands.
"""
import logging
from random import choice

from discord.ext import commands

from utils.database import get_quote, set_quote

client = commands.Bot(command_prefix='~')
logger = logging.getLogger(__name__)

quote_id_stack = []

@client.command(aliases=['q'])
async def quote(bot: object, *quote: str) -> str:
    """
    Save a quote into database.
    """
    if not quote:
        return await bot.send('Insert a message to save.')

    quote = ' '.join(quote)

    try:
        user = bot.author.name
        set_quote(user, quote)
    except Exception as ex:
        return await bot.send(ex.args)
    else:
        return await bot.send('Done:\n`%s`' % quote)


@client.command(aliases=['rq'])
async def random_quote(bot: object) -> str:
    """
    Get an random quote from database.
    """
    while chosen_one[2] in quote_id_stack:
        quotes = get_quote()
        chosen_one = choice(quotes)

        quote_id_stack.add(chosen_one[2])

    if len(quote_id_stack) >= 5:
        quote_id_stack[0].pop()

    try:
        return await bot.send(f'{chosen_one[0]}\n`By: {chosen_one[1]}`')
    except Exception as ex:
        return await bot.send(ex)

@client.command(aliases=['qstack'])
async def queue_stack(bot: object) -> str:
    """
    Displays the 5 quote history stack
    """
    id_stack = ""
    for qid in quote_id_stack:
        id_stack = id_stack + qid

    rmessage = "A list of the 5 latest message IDs follows: " + id_stack

    return await bot.send(rmessage)

