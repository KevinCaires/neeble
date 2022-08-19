"""
Database utils module.
"""
import logging

import MySQLdb
from models.quotes import Quotes
from settings.config import MYSQL_CONFIG, SQLACHEMY
from sqlalchemy import select
from sqlalchemy.orm import Session

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
    with Session(SQLACHEMY) as session:
        session.add(Quotes(
            quote=quote,
            user=user,
        ))
        session.commit()


def get_quotes(ids: list) -> tuple:
    """
    Get the saved quotes.
    ids: List of quote ID's
    """
    with Session(SQLACHEMY) as session:
        _sql = select(Quotes).where(Quotes.id.not_in(ids))
        return [item for item in session.scalars(_sql)]


def get_by_id(id: int) -> object:
    """
    Get one quote by ID.
    """
    with Session(SQLACHEMY) as session:
        result = [s for s in session.query(Quotes).filter(Quotes.id==id)]
        return result[0] if result else None


def remove_quote(_id: int) -> bool:
    """
    Delete one quote by database ID.
    """
    try:
        with Session(SQLACHEMY) as session:
            item = get_by_id(_id)
            session.delete(item)
            session.commit()
        return True
    except Exception:
        return False


def count_quotes() -> int:
    """
    Counts the amount of quotes in the database
    """
    with Session(SQLACHEMY) as session:
        response = session.query(Quotes.id).count()
    return response
