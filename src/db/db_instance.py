import pymssql

from config import Config
from src.common.des import des_decrypt
import ast


class Configuration(object):
    host = ""
    port = 0
    user = ""
    pwd = ""
    db = ""

    def __init__(self):
        con = des_decrypt(Config.conn_string)
        dict_str = str(con, encoding='utf-8')
        db_dict = ast.literal_eval(dict_str)

        self.host = db_dict['host']
        self.port = db_dict['port']
        self.user = db_dict['user']
        self.db = db_dict['db']
        self.pwd = db_dict['pwd']
    pass


class UniqueObject:
    """description of class"""
    cur = None
    conn = None

    def __del__(self):
        if not self.conn:
            self.conn.close()
            print(">>>>>>>>>>>>>>>>>Connection has been closed!<<<<<<<<<<<<<<<<<<<")

    @staticmethod
    def get_object():
        if not UniqueObject.cur:
            print(">>>>>>>>>>>>>>>>>Connecting to Database.....<<<<<<<<<<<<<<<<<<")
            return UniqueObject.get_connect()
        return UniqueObject.conn, UniqueObject.cur

    @staticmethod
    def get_connect():
        db_config = Configuration()
        if not db_config.db:
            raise (NameError, "no db Info")
        UniqueObject.conn = pymssql.connect(host=db_config.host, port=db_config.port,
                                            user=db_config.user, password=db_config.pwd,
                                            database=db_config.db, charset="utf8")
        UniqueObject.cur = UniqueObject.conn.cursor(as_dict=True)
        if not UniqueObject.cur:
            raise (NameError, "Connection error!")
        else:
            return UniqueObject.conn, UniqueObject.cur
