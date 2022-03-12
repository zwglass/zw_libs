import sys
from pathlib import Path
import time

self_file_path = str(Path(__file__).resolve())
project_folder_path = str(Path(self_file_path).parent.parent)
sys.path.append(project_folder_path)
# print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},")

# 新增操作
from _base_funcs.dict_convert_sql import DictConvertSqlText
from _base_funcs.connect_db import ConnectDb
from _db_handle.get import DbGet

class DbInsert(object):
    """
    数据库插入操作类
    db_types = ['sqlite3', 'postgresql']
    sqlite3: connect_args = {'sqlite3_file_path': ''}; postgresql: connect_args = {'db_name', 'user_name', 'password', 'host':'127.0.0.1', 'port':'5432'};
    """
    def __init__(self, db_type='sqlite3', **connect_args) -> None:
        super().__init__()
        self.dict_convert_sql_text_class = DictConvertSqlText()
        self.connect_db_class = ConnectDb()
        self.db_type = db_type
        self.connect_args = connect_args

    def insert_default_dict(self, columns):
        # insert默认值 dict
        default_dict = {}
        for col in columns:
            col_name = col.get('column_name', '')
            col_props = col.get('column_props', {})
            if col_name == '':
                continue
            default_val = col_props.get('default', '')
            if default_val == 'int(time.time())':
                default_val = int(time.time())
            default_dict.update({col_name: default_val})
        return default_dict

    def insert(self, table_name, columns, **insert_dict):
        # 新增操作 columns: configs -> columns
        default_dict = self.insert_default_dict(columns)
        default_dict.update(insert_dict)

        convert_insert_dict = self.dict_convert_sql_text_class.dict_convert_insert_str(self.db_type, **default_dict)
        columns = convert_insert_dict['columns']
        placeholders = convert_insert_dict['placeholders']
        values_tuple = convert_insert_dict['values_tuple']
        sql = f"insert into {table_name} ({columns}) values ({placeholders})"
        # print(sql, values_tuple)
        conn = self.connect_db_class.connect_db(self.db_type, **self.connect_args)

        # 获得游标对象，一个游标对象可以对数据库进行执行操作
        cursor = conn.cursor()
        # 执行语句
        cursor.execute(sql, values_tuple)
        # 事物提交
        conn.commit()
        # 关闭数据库连接
        conn.close()
        return self.query_inserted_data(table_name, **insert_dict)

    def query_inserted_data(self, table_name, **insert_dict):
        # 查询新增数据
        # print(F"File \"{self_file_path}\", line {sys._getframe().f_lineno}, ", insert_dict)
        db_get_class = DbGet(self.db_type, **self.connect_args)
        result = db_get_class.query(table_name, 0, 20, True, **insert_dict)
        # print(result)
        return result['results'][0]
