"""
Database utils module.
"""
import logging
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

def get_quote() -> tuple:
    """
    Get the saved quotes.
    """
    _sql = f'''
        select quote, user, id
        from neeble_quotes;
    '''
    response = None
    with Cursor(MYSQL_CONFIG) as cursor:
        cursor.execute(_sql)
        response = cursor.fetchall()
    return response
