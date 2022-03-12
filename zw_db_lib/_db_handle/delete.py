import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve())
project_folder_path = str(Path(self_file_path).parent.parent)
sys.path.append(project_folder_path)
# print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},")

# 删除操作
from _base_funcs.dict_convert_sql import DictConvertSqlText
from _base_funcs.connect_db import ConnectDb

class DbDelete(object):
    """
    更新操作 根据 id 更新
    db_types = ['sqlite3', 'postgresql']
    sqlite3: connect_args = {'sqlite3_file_path': ''}; postgresql: connect_args = {'db_name', 'user_name', 'password', 'host':'127.0.0.1', 'port':'5432'};
    """
    def __init__(self, db_type='sqlite3', **connect_args) -> None:
        super().__init__()
        self.dict_convert_sql_text_class = DictConvertSqlText()
        self.connect_db_class = ConnectDb()
        self.db_type = db_type
        self.connect_args = connect_args

    def delete(self, table_name, id):
        # 删除操作
        conn = self.connect_db_class.connect_db(self.db_type, **self.connect_args)
        placeholder_str = self.dict_convert_sql_text_class.sql_placeholder_str(self.db_type)
        sql = f"delete from {table_name} where id = {placeholder_str};"
        # print(sql)
        # 获得游标对象，一个游标对象可以对数据库进行执行操作
        cursor = conn.cursor()
        # 执行语句
        cursor.execute(sql, (id, ))
        # 事物提交
        conn.commit()
        # 关闭数据库连接
        conn.close()

    def delete_multiple(self, table_name, **query_factor):
        # 批量删除操作
        conn = self.connect_db_class.connect_db(self.db_type, **self.connect_args)
        placeholder_str = self.dict_convert_sql_text_class.sql_placeholder_str(self.db_type)
        sql = f"delete from {table_name}"
        query_dict = self.dict_convert_sql_text_class.dict_convert_query_where_string(self.db_type, **query_factor)
        where_str = query_dict.get('where_str', '')
        values_tuple = query_dict.get('values_tuple', tuple())
        if len(where_str) > 0:
            sql += f" where {where_str};"
        # print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},", sql, values_tuple)
        # 获得游标对象，一个游标对象可以对数据库进行执行操作
        cursor = conn.cursor()
        # 执行语句
        cursor.execute(sql, values_tuple)
        # 事物提交
        conn.commit()
        # 关闭数据库连接
        conn.close()
        return
