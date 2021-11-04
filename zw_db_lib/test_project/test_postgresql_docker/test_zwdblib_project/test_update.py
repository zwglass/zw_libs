# 测试查询
import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.append(self_file_path)

from _db_handle.put import DbUpdate


class TestUpdateDb(object):
    """test query"""

    def __init__(self) -> None:
        super().__init__()
        # self.query_table_columns_class = QueryTableColumns()
        # self.sqlite_db_path = '/Users/zhaoshenghua/development/shell_text/db/zw_db_lib/test_project/test_db.sqlite3'
        self.conn_factor = {'db_name': 'postgres', 'user_name': 'zwglass', 'password': 'zw123456', 'host':'db_postgres_rebate_platform', 'port':'5432'}
        self.db_update_class = DbUpdate('postgresql', **self.conn_factor)

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

