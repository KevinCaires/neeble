"""
Database utils module.
"""
import logging
from collections import namedtuple

import MySQLdb
from settings.config import MYSQL_CONFIG

logger = logging.getLogger(__name__)


class Cursor:
    """
    Context manage for database handler.
    """
    def __init__(self, config: dict) -> None:
        """
        Constructor.
        """
        self.configuration = config

    def __enter__(self) -> 'cursor':
        """
        Context manager.
        """
        self.conn = MySQLdb.connect(**self.configuration)
        self.cursor = self.conn.cursor()

        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        """
        Exit from context manager.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


def migrate() -> None:
    """
    Create tables.
    """
    _sql = '''
        create table if not exists neeble_quotes(
            id int auto_increment primary key,
            user varchar(200) not null,
            quote varchar(500) not null unique,
            index quote_idx (quote)
        );
    '''
    try:
        with Cursor(MYSQL_CONFIG) as cursor:
            cursor.execute(_sql)
    except Exception as ex:
        logger.error(ex.args)


def set_quote(user: str, quote: str) -> None:
    """
    Set a quote into database.
    """
    _sql = f'''
        insert into neeble_quotes(user, quote)
        value("{user}", "{quote}");
    '''
    with Cursor(MYSQL_CONFIG) as cursor:
        cursor.execute(_sql)

def get_quotes(ids: list) -> tuple:
    """
    Get the saved quotes.
    ids: List of quote ID's
    """
    _sql = f'''
        select quote, user, id
        from neeble_quotes
    '''
    _sql = _sql + f' where id not in ({",".join([str(id) for id in ids])});' if ids else _sql + ';'
    response = []
    obj = namedtuple('Quotes', ['quote', 'user', 'id'])

    with Cursor(MYSQL_CONFIG) as cursor:
        cursor.execute(_sql)
        response = cursor.fetchall()

    return tuple(obj(*r) for r in response)


def get_by_id(id: int) -> object:
    """
    Get one quote by ID.
    """
    obj = namedtuple('Quotes', ['quote', 'user', 'id'])
    _sql = f'''
        select quote, user, id
        from neeble_quotes
        where id={id};
    '''

    with Cursor(MYSQL_CONFIG) as cursor:
        cursor.execute(_sql)
        quote = cursor.fetchone()

    if not quote:
        return None

    return obj(*quote)

def remove_quote(_id: int) -> bool:
    """
    Delete one quote by database ID.
    """
    _sql = f'''
        delete from neeble_quotes
        where id={_id};
    '''

    try:
        with Cursor(MYSQL_CONFIG) as cursor:
            cursor.execute(_sql)
        return True
    except Exception:
        return False

def count_quotes() -> int:
    """
    Counts the amount of quotes in the database
    """
    _sql = f'''
        select count(*) from neeble_quotes
    '''

    with Cursor(MYSQL_CONFIG) as cursor:
        cursor.execute(_sql)
        count = cursor.fetchone()
    
    return count