"""
Bot commands.
"""
import logging
from random import choice

from discord.ext import commands

from utils.database import get_quotes, set_quote

client = commands.Bot(command_prefix='--')
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
        quote = quote.encode('utf-8')
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
    quotes = get_quotes(quote_id_stack)
    stack_len = len(quote_id_stack)

    if not quotes and stack_len > 0:
        quote_id_stack.pop(0)
        quotes = get_quotes(quote_id_stack)
    elif not quotes:
        return await bot.send('Have no one quote saved.')

    chosen_one = choice(quotes)
    quote_id_stack.append(chosen_one.id)

    if stack_len >= 5:
        quote_id_stack.pop(0)

    try:
        # To image links.
        if 'http' in chosen_one.quote:
            return await bot.send(f'{chosen_one.quote.encode("utf-8")}')
        return await bot.send(f'{chosen_one.quote}\n`By: {chosen_one.user}`')

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
