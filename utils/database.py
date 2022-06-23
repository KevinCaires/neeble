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
        self.conn = MySQLdb.connect(**self.configuration, charset='utf-8')
        self.cursor = self.conn.cursor()

        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        """
        Exit from context manager.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class DataBase:
    """
    Database handler.
    """
    @staticmethod
    def migrate() -> None:
        """
        Create tables.
        """
        _sql = '''
            create if not exists neeble_quotes(
                user varchar(200) not null,
                quote varchar(1000) not null unique
            );
        '''
        try:
            with Cursor(MYSQL_CONFIG) as cursor:
                cursor.execute(_sql)
        except Exception as ex:
            logger.error(ex.args[0])
