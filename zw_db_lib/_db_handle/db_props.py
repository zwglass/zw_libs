import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve())
project_folder_path = str(Path(self_file_path).parent.parent)
sys.path.append(project_folder_path)
# print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},")

# 数据库属性查询
from _base_funcs.load_table_columns import LoadTableColumns
from _base_funcs.connect_db import ConnectDb

class QueryTableColumns(object):
    """
    查询数据库属性
    """

    def __init__(self) -> None:
        super().__init__()
        self.load_table_columns_class = LoadTableColumns()
        self.connect_db_class = ConnectDb()

    def query_columns(self, db_type_key, table_name, **kwargs):
        '''
        查询表所有列
        db_type_key in ['sqlite3', 'postgresql']
        sqlite3: kwargs = {'sqlite3_file_path': ''}
        postgresql: kwargs = {'db_name', 'user_name', 'password', 'host':'127.0.0.1', 'port':'5432'}
        '''
        conn = self.connect_db_class.connect_db(db_type_key, **kwargs)
        columns = self.load_table_columns_class.load_columns(db_type_key, table_name, conn)
        return columns
