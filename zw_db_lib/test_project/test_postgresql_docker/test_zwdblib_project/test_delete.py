# 测试删除
import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(self_file_path)

# from _db_handle.db_props import QueryTableColumns
from _db_handle.delete import DbDelete

class TestDeleteDb(object):
    """test delete"""
    def __init__(self) -> None:
        super().__init__()
        # self.query_table_columns_class = QueryTableColumns()
        self.sqlite_db_path = '/Users/zhaoshenghua/development/shell_text/db/zw_db_lib/test_project/test_db.sqlite3'
        self.db_delete_class = DbDelete('sqlite3', **{'sqlite3_file_path': self.sqlite_db_path})

    def test_delete_data(self):
        # 测试删除
        table_name = 'assist_taobao_platform_platformgoods'
        # query_factor = {'goods_title__contains': 'test', 'goods_code': '', 'platform_code__in': [1,2,]}
        delete_id = 1
        self.db_delete_class.delete(table_name, delete_id)


if __name__ == '__main__':
    test_delete_db_class = TestDeleteDb()
    test_delete_db_class.test_delete_data()