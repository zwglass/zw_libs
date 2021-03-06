import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve())
project_folder_path = str(Path(self_file_path).parent.parent)
sys.path.append(project_folder_path)
# print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},")

# 更新操作
from _base_funcs.dict_convert_sql import DictConvertSqlText
from _base_funcs.connect_db import ConnectDb
from _db_handle.get import DbGet

class DbUpdate(object):
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

    def update(self, table_name, **update_dict):
        # 更新操作 update_dict: 必须包含id 根据id更新
        # print(self.db_type)
        update_id = update_dict.get('id', 0)
        convert_update_dict = self.dict_convert_sql_text_class.dict_convert_update_str(self.db_type, **update_dict)
        update_str = convert_update_dict.get('update_str', '')
        values_tuple = convert_update_dict.get('values_tuple', ())
        sql = f"update {table_name} set {update_str} where id = {update_id};"
        conn = self.connect_db_class.connect_db(self.db_type, **self.connect_args)
        # print(sql)
        # 获得游标对象，一个游标对象可以对数据库进行执行操作
        cursor = conn.cursor()
        # 执行语句
        cursor.execute(sql, values_tuple)
        # 事物提交
        conn.commit()
        # 关闭数据库连接
        conn.close()

        return self.query_data(table_name, **{'id': update_id})

    def query_data(self, table_name, **query_dict):
        # 查询新增数据
        # print(F"File \"{self_file_path}\", line {sys._getframe().f_lineno}, ", insert_dict)
        db_get_class = DbGet(self.db_type, **self.connect_args)
        result = db_get_class.query(table_name, 0, 20, True, **query_dict)
        return result['results'][0]
