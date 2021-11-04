import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve())
project_folder_path = str(Path(self_file_path).parent.parent)
sys.path.append(project_folder_path)
# print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},")

from _base_funcs.configs import db_types

# 读取表的列

class LoadTableColumns(object):
    """
    读取表的列
    """
    def __init__(self) -> None:
        super().__init__()

    def load_columns(self, db_type_key, table_name, db_connect):
        '''查询表的列'''
        conn_attr_name = db_types.get(db_type_key, '')
        if len(conn_attr_name) < 2:     # 不支持的数据库 抛出错误和提示
            support_dbs = str(db_types.keys())
            print(f"File \"{db_type_key}\", line {sys._getframe().f_lineno}, {db_type_key} 数据库类型不支持(支持的数据库: {support_dbs})...")
            raise ZeroDivisionError(f'数据库类型不支持(支持的数据库: {support_dbs})...')

        func = getattr(self, 'load_columns_' + conn_attr_name)
        return func(table_name, db_connect)

    def load_columns_sqlite3(self, table_name, db_connect):
        # sqlite3 读取表的列 return: (index, 列包括列名, 数据类型, 该列是否可以为NULL, 该列的默认值)
        sql_query_columns = f"PRAGMA table_info([{table_name}])"
        cursor1 = db_connect.cursor()
        all_columns = cursor1.execute(sql_query_columns)
        all_columns_list = []
        for c in all_columns:
            all_columns_list.append(c)
        return all_columns_list

    def load_columns_postgresql(self, table_name, db_connect):
        # postgresql 读取表的列 return: (index, 列名, 数据类型, 该列是否可以为NULL, 该列的默认值)
        # sql_query_columns = f"SELECT * FRON information_schema.columns WHERE table_schema=\'public\' AND table_name=\'{table_name}\';"
        
        sql_query_columns = f"select ordinal_position, column_name, data_type, is_nullable, column_default from information_schema.columns where table_schema='public' and table_name=\'{table_name}\';"
        # print(sql_query_columns)
        cursor1 = db_connect.cursor()           # 使用cursor()方法创建游标对象
        cursor1.execute(sql_query_columns)      # 使用execute()方法执行MYSQL函数

        # 使用fetchone()方法获取单行 fetchall()获取多行。
        columns = cursor1.fetchall()
        ret_columns = []
        for column_tup in columns:          # 让 index 从 1 开始
            current_c_tup = list(column_tup)
            current_c_tup[0] = current_c_tup[0] - 1
            ret_columns.append(current_c_tup)
        return ret_columns
