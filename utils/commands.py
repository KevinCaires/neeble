"""
Bot commands.
"""
import logging
from random import choice

from discord.ext import commands

from utils.database import get_quote, set_quote

client = commands.Bot(command_prefix='~')
logger = logging.getLogger(__name__)


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
    quotes = get_quote()
    chosen_one = choice(quotes)

    try:
        return await bot.send(f'{chosen_one[0]}\n`By: {chosen_one[1]}`')
    except Exception as ex:
        return await bot.send(ex)
