import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve())
project_folder_path = str(Path(self_file_path).parent.parent)
sys.path.append(project_folder_path)
# print(f"File \"{self_file_path}\", line {sys._getframe().f_lineno},")

# 查询操作
from _base_funcs.dict_convert_sql import DictConvertSqlText
from _base_funcs.connect_db import ConnectDb
from _db_handle.db_props import QueryTableColumns

class DbGet(object):
    """
    数据库查询操作类
    db_types = ['sqlite3', 'postgresql']
    sqlite3: connect_args = {'sqlite3_file_path': ''}; postgresql: connect_args = {'db_name', 'user_name', 'password', 'host':'127.0.0.1', 'port':'5432'};
    """
    def __init__(self, db_type='sqlite3', **connect_args) -> None:
        super().__init__()
        self.dict_convert_sql_text_class = DictConvertSqlText()
        self.connect_db_class = ConnectDb()
        self.query_table_columns_class = QueryTableColumns()
        self.db_type = db_type
        self.connect_args = connect_args

    def query(self, table_name, pagination = 0, data_lines_number = 10, desc = False, order_by_columns = ['id', ], **query_factor):
        # 查询操作 
        # pagination: 0-查询所有数据, >0-分页查询;
        # data_lines_number: 每页数据数量
        # desc: 是否降序排列, default=False
        # order_by_columns: 排序的列 默认 id 排序
        # query_factor: 查寻条件
        conn = self.connect_db_class.connect_db(self.db_type, **self.connect_args)
        query_dict = self.dict_convert_sql_text_class.dict_convert_query_where_string(self.db_type, **query_factor)
        where_str = query_dict.get('where_str', '')
        values_tuple = query_dict.get('values_tuple', tuple())
        sql = f"select * from {table_name} where {where_str}"
        if where_str == '':
            sql = f"select * from {table_name}"

        if order_by_columns:
            order_by_strs = ''
            for c in order_by_columns:
                if desc:
                    order_by_strs = f"{order_by_strs}, {c} desc"    # 倒序
                else:
                    order_by_strs = f"{order_by_strs}, {c}"    # 顺序
            order_by_strs = order_by_strs.strip(', ')
            sql = sql + ' order by ' + order_by_strs

        if pagination > 0:
            # 分页查询
            offset_number = (pagination - 1) * data_lines_number
            sql = f"{sql} limit {data_lines_number} offset {offset_number}"
        sql = sql + ';'
        
        # print(sql, values_tuple)
        cur = conn.cursor()
        cur.execute(sql, values_tuple)
        query_list = cur.fetchall()
        return self.query_results_convert_dicts(table_name, *query_list)

    def query_results_convert_dicts(self, table_name, *queried_list):
        # 查询到tuple convert dict
        ret_list = []
        columns = self.query_table_columns_class.query_columns(self.db_type, table_name, **self.connect_args)
        for queried_tuple in queried_list:
            ret_list.append(self.queried_tuple_convert_dict(queried_tuple, columns))
        return ret_list

    def queried_tuple_convert_dict(self, queried_tuple, columns):
        # 查询tuple转换为 dict
        ret_dict = {}
        for column in columns:
            c_index = column[0]
            c_name = column[1]
            ret_dict.update({ c_name: queried_tuple[c_index] })
        return ret_dict

    # def serialize(self, columns, query_result):
    #     """
    #     序列化 查询结果转dict
    #     Transforms a model into a dictionary which can be dumped to JSON.
    #     """
    #     # first we get the names of all the columns on your model
    #     # then we return their values in a dict
    #     return dict((c, getattr(model, c)) for c in columns)
