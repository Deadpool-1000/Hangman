import logging
import sqlite3
import shortuuid
import hashlib
from datetime import datetime

from src.DBUtils.database import Database
from src.config import get_settings
from src.config.api.api_config import get_api_config
from src.config.queries.queries_config import get_queries_config


queries_config = get_queries_config()
settings = get_settings()
api_config = get_api_config()


logger = logging.getLogger('main.init_db')


def init_db():
    db = Database()
    try:
        db.connect()

        cur = db.connection.cursor()
        create_tables(cur)

        # admin-data
        admin_id = shortuuid.ShortUUID().random(length=5)
        pwd = hashlib.sha256(settings.admin_password.encode()).hexdigest()
        cur.execute(queries_config.INSERT_INTO_AUTH, (admin_id, settings.admin_name, pwd, api_config.ADMIN))
        cur.execute(queries_config.INSERT_INTO_PLAYERS, (admin_id, datetime.now()))

        game_configurations = [
            (1, 'ROUND', 'OPTION1', 1),
            (2, 'ROUND', 'OPTION2', 3),
            (3, 'ROUND', 'OPTION3', 6),
            (4, 'DIFFICULTY', 'EASY', 8),
            (5, 'DIFFICULTY', 'MEDIUM', 10),
            (6, 'DIFFICULTY', 'HARD', 12)
        ]
        # default game configurations available
        cur.executemany(queries_config.INSERT_INTO_GAME_CONFIG, game_configurations)

    except sqlite3.IntegrityError:
        logger.info('Database already initialized. Re-initialization caused integrity error.')
    except sqlite3.Error:
        logger.error("There was a problem connecting to database.")
    except sqlite3.OperationalError:
        logger.error('There was an operational problem connecting to database. ')
    finally:
        db.close()


def create_tables(cur):
    cur.execute(queries_config.CREATE_TABLE_QUERY)
    cur.execute(queries_config.CREATE_TABLE_AUTH)
    cur.execute(queries_config.CREATE_TABLE_PLAYER)
