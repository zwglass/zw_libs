# 测试查询
import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.append(self_file_path)

from _db_handle.get import DbGet


class TestQueryDb(object):
    """test query"""

    def __init__(self) -> None:
        super().__init__()
        # self.query_table_columns_class = QueryTableColumns()
        self.sqlite_db_path = '/Users/zhaoshenghua/development/shell_text/db/zw_db_lib/test_project/test_db.sqlite3'
        self.conn_factor = {'db_name': 'postgres', 'user_name': 'zwglass', 'password': 'zw123456', 'host':'db_postgres_rebate_platform', 'port':'5432'}
        self.db_get_class = DbGet('postgresql', **self.conn_factor)

    def test_query(self):
        # 查询
        db_path = 'test_project/test_db.sqlite3'

    def test_query_columns(self):
        # 查询列
        table_name = 'assist_taobao_platform_platformgoods'
        query_kwargs = {'sqlite3_file_path': self.sqlite_db_path}
        # columns = self.query_table_columns_class.query_columns('sqlite3', table_name, **query_kwargs)
        # return columns

    def test_query_data(self):
        # 查询测试
        table_name = 'assist_taobao_platform_platformgoods'
        # query_factor = {'goods_title__contains': 'test', 'goods_code': '', 'platform_code__in': [1,2,]}
        query_factor = {'goods_title__endwith': '001', 'platform_code': 1}
        results = self.db_get_class.query(table_name, **query_factor)
        return results


if __name__ == '__main__':
    test_query_db_class = TestQueryDb()
    # columns = test_query_db_class.test_query_columns()
    # print(columns)

    results = test_query_db_class.test_query_data()
    print(results)
