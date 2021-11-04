# 测试更新
import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(self_file_path)

# from _db_handle.db_props import QueryTableColumns
from _db_handle.put import DbUpdate

class TestUpdateDb(object):
    """test update"""

    def __init__(self) -> None:
        super().__init__()
        # self.query_table_columns_class = QueryTableColumns()
        self.sqlite_db_path = '/Users/zhaoshenghua/development/shell_text/db/zw_db_lib/test_project/test_db.sqlite3'
        self.db_update_class = DbUpdate('sqlite3', **{'sqlite3_file_path': self.sqlite_db_path})

    def test_update_data(self):
        # 查询测试
        table_name = 'assist_taobao_platform_platformgoods'
        # query_factor = {'goods_title__contains': 'test', 'goods_code': '', 'platform_code__in': [1,2,]}
        update_id = 1
        update_dict = {'goods_code': 'code_test 001'}

        self.db_update_class.update(table_name, update_id, **update_dict)


if __name__ == '__main__':
    test_update_db_class = TestUpdateDb()
    test_update_db_class.test_update_data()
