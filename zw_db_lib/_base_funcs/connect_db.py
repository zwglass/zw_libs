import sqlite3
import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve())
project_folder_path = str(Path(self_file_path).parent.parent)
sys.path.append(project_folder_path)
# print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},")

from _base_funcs.configs import db_types

# psycopg2 需要先 pip install psycopg2
# on Mojave macOS, I solved it by running below steps: pip uninstall psycopg2, pip install psycopg2-binary
# 连接数据库

class ConnectDb(object):
    """
    连接数据库
    """
    def __init__(self) -> None:
        super().__init__()

    def connect_db(self, db_type_key, **connect_args):
        '''连接数据库, 判断哪种数据库, 直接连接 kwargs={'sqlite3_file_path': '', 'db_name': '', ...}'''
        conn_attr_name = db_types.get(db_type_key, '')
        if len(conn_attr_name) < 2:     # 不支持的数据库 抛出错误和提示
            support_dbs = str(db_types.keys())
            print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno}, {db_type_key} 数据库类型不支持(支持的数据库: {support_dbs})...")
            raise ZeroDivisionError(f'数据库类型不支持(支持的数据库: {support_dbs})...')
        
        conn_attr_name = 'connect_' + conn_attr_name
        conn_func = getattr(self, conn_attr_name)
        return conn_func(**connect_args)

    def connect_sqlite3(self, **connect_args):
        # 连接sqlite3; kwargs = {'sqlite3_file_path': ''}
        sqlite3_file_path = connect_args.get('sqlite3_file_path')
        conn = sqlite3.connect(sqlite3_file_path)
        return conn

    def connect_postgresql(self, **connect_args):
        import psycopg2
        # 连接 postgreSQL; kwargs = {'db_name', 'user_name', 'password', 'host':'127.0.0.1', 'port':'5432'}
        db_name = connect_args.get('db_name', '')
        user_name = connect_args.get('user_name', '')
        password = connect_args.get('password', '')
        host = connect_args.get('host', '127.0.0.1')
        port = connect_args.get('port', '5432')

        conn = psycopg2.connect(database=db_name, user=user_name, password=password, host=host, port=port)
        return conn


