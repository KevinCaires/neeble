"""
Bot commands.
"""
import logging
from random import choice

from discord.ext import commands

from utils.database import get_by_id, get_quotes, set_quote

client = commands.Bot(command_prefix='--')
logger = logging.getLogger(__name__)

quote_id_stack = []

@client.command(aliases=['q'])
async def quote(bot: object, *quote: str) -> str:
    """
    Save a quote into database.
    """
    if not quote:
        return await bot.send('Insert a message to save.\n_Your dumb ass!_')

    quote = ' '.join(quote)

    if 'http' in quote and 'discord' in quote and not quote[-4:] == '.png':
        return await bot.send("- _Don't fuck, dumb ass!_\n"\
            "- _Hey put a valid image link, bitch!_\n- _Are you an idiot? You mother fucker!_")

    try:
        user = bot.author.name
        set_quote(user, quote)
    except Exception as ex:
        return await bot.send(f'{ex.args}\n_What that fuck you doing?_')
    else:
        return await bot.send('Done:\n`%s`' % quote)


@client.command(aliases=['rq'])
async def random_quote(bot: object) -> str:
    """
    Get an random quote from database.
    """
    quotes = get_quotes(quote_id_stack)
    stack_limit = int((len(quotes) * .5))
    stack_len = len(quote_id_stack)

    if not quotes and stack_len > 0:
        quote_id_stack.pop(0)
        quotes = get_quotes(quote_id_stack)
    elif not quotes:
        return await bot.send('Have no one quote saved.\n_Hey jerk, coffee?_')

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


@client.command(aliases=['bid'])
async def by_id(bot, _id: int=None) -> str:
    """
    Get quote by ID.
    """
    if not isinstance(_id, int) or not _id:
        return await bot.send("_Don't fuck, you ass hole_.\nThe ID need to be a interger!")

    quote = get_by_id(_id)

    if not quote:
        return await bot.send("_Got wrong, you socker!_\nThis ID doesn't exist in database!")

    try:
        # To image links.
        if 'http' in quote.quote:
            return await bot.send(f'{quote.quote}')
        return await bot.send(f'{quote.quote}\n`By: {quote.user}`')

    except Exception as ex:
        return await bot.send(ex)


@client.command(aliases=['qstack'])
async def queue_stack(bot: object) -> str:
    """
    Displays the 5 quote history stack
    """
    return await bot.send('A list of the 5 latest message IDs follows:'\
        f' `{",".join(str(q) for q in quote_id_stack[-5:])}`')
