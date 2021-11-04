# 测试插入
import sys
from pathlib import Path

self_file_path = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.append(self_file_path)

from _db_handle.post import DbInsert

class TestDbInsert(object):
    """test query"""

    def __init__(self) -> None:
        super().__init__()
        self.conn_factor = {'db_name': 'postgres', 'user_name': 'zwglass', 'password': 'zw123456', 'host':'db_postgres_rebate_platform', 'port':'5432'}
        self.db_insert_class = DbInsert('postgresql', **self.conn_factor)

    def insert_data(self):
        # 测试插入数据
        table_name = 'assist_taobao_platform_platformgoods'
        columns = [
            # id 自动生成
            {'column_name': 'platform_code', 'column_type': 'IntegerField', 'column_props': { 'verbose_name': '平台编号: 0=未知, 1-淘宝天猫, 2-京东, 3-拼多多, 4-苏宁易购', 'default': 0 }},
            {'column_name': 'goods_title', 'column_type': 'CharField', 'column_props': { 'verbose_name': '商品标题', 'default': 0 }},
            {'column_name': 'goods_code', 'column_type': 'CharField', 'column_props': { 'verbose_name': '商品编号', 'default': '' }},
            {'column_name': 'goods_json_info', 'column_type': 'TextField', 'column_props': { 'verbose_name': '商品详情, 商品json字符串', 'default': '' }},
            {'column_name': 'add_time', 'column_type': 'IntegerField', 'column_props': { 'verbose_name': '创建时间戳', 'default': 0 }},
            {'column_name': 'update_time', 'column_type': 'IntegerField', 'column_props': { 'verbose_name': '最后更新时间戳', 'default': 0 }},
            {'column_name': 'explains', 'column_type': 'CharField', 'column_props': { 'verbose_name': '说明', 'default': '' }},

        ]
        insert_kwargs = {'platform_code': 1, 'goods_title': 'test goods002', 'goods_code': 'ABC_test_goods_002'}

        self.db_insert_class.insert(table_name, columns, **insert_kwargs)


if __name__ == '__main__':
    test_db_insert_class = TestDbInsert()
    test_db_insert_class.insert_data()
