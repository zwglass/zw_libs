import sys
from pathlib import Path

self_file_path = Path(__file__).resolve()
project_folder_path = str(self_file_path.parent.parent.parent.parent)
sys.path.append(project_folder_path)

from _base_funcs.load_table_columns import LoadTableColumns
from _base_funcs.connect_db import ConnectDb


if __name__ == '__main__':
    # test query postgresql table columns
    connect_db_class = ConnectDb()
    load_table_columns_class = LoadTableColumns()

    db_type_key = 'postgresql'
    table_name = 'assist_taobao_platform_platformgoods'
    conn_factor = {'db_name': 'postgres', 'user_name': 'zwglass', 'password': 'zw123456', 'host':'db_postgres_rebate_platform', 'port':'5432'}
    conn = connect_db_class.connect_db(db_type_key, **conn_factor)
    columns = load_table_columns_class.load_columns(db_type_key, table_name, conn)
    print(columns)
