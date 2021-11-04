import copy


# dict 转 sql

"""
# __gt: >;  __gte: >=;
ret=models.Person.objects.filter(id__gt =1)  # id>1的结果

# __lt: <; lte: <=;
ret=models.Person.objects.filter(id__lt =4)  # id<4的结果

# __in: 列表中包含的内容;
ret=models.Person.objects.filter(id__in =[1,3])  # id 为1,3 的结果

# __range: 之间的值
ret=models.Person.objects.filter(id__range=[1,3])  # 1=< id <=3 的结果; 相当于filter(id__gt =1, id__lt=3)

# __contains: 字符串包含,忽律大小写
ret=models.Person.objects.filter ( name__contains='e')  # name中包含 'e'的 结果

# __startwith: 开头包含, 忽律大小写; __endwith: 结尾包含, 忽律大小写
ret=models.Person.objects.filter(name__startwith='e')  # name中以 'e'开头的结果

# __isnull: 为空的字段
name__isnull=True  # 取出name字段为空的 (待完善)
"""


class DictConvertSqlText(object):

    def __init__(self) -> None:
        super().__init__()
        self.placeholder_str_dict = {'sqlite3': '?', 'postgresql': '%s'}

    def sql_placeholder_str(self, db_type_key):
        # sql 占位符
        use_placeholder_str = self.placeholder_str_dict.get(db_type_key, '')
        if use_placeholder_str == '':
            # 占位符不支持抛出错误
            raise ZeroDivisionError(f'数据库类型不支持: {db_type_key}')
        return use_placeholder_str

    def key_convert_sql_result(self, key_val, val_val, placeholder_str):
        # 字典key符合结果 val_val 使用占位符去掉引号
        sign_results_gt_lt = { 'gt': '>', 'gte': '>=', 'lt': '<', 'lte': '<=', 'ne': '<>' }

        sign_results_in = { 'in': 'LIKE' }
        sign_results_range = { 'range': 'BETWEEN' }
        sign_results_contains = { 'contains': 'LIKE' }      # 包含
        sign_results_start_with = { 'startwith': 'LIKE' }
        sign_results_end_with = { 'endwith': 'LIKE' }

        key_list = key_val.split('__', 1)
        # val_val = f"\'{val_val}\'"
        sql_string = f"{key_list[0]} = {placeholder_str}"
        values_list = [ copy.deepcopy(val_val), ]
        if len(key_list) == 2:
            if key_list[1] in sign_results_gt_lt.keys():        # 大于小于 符号
                current_sign = sign_results_gt_lt[key_list[1]]
                sql_string = f"{key_list[0]} {current_sign} {placeholder_str}"
            if key_list[1] in sign_results_in.keys() and len(val_val) > 0:      # 包含 符号
                sql_string = ''
                values_list = []
                for current_val in val_val:
                    values_list.extend([current_val, ])
                    if len(sql_string) > 1:
                        sql_string = f"{sql_string} or {key_list[0]} like {placeholder_str}"
                    else:
                        sql_string = f"{key_list[0]} like {placeholder_str}"
            if key_list[1] in sign_results_range.keys() and len(val_val) == 2:
                sql_string = f"{key_list[0]} between {placeholder_str} and {placeholder_str}"
                values_list = [ val_val[0], val_val[1], ]
            if key_list[1] in sign_results_contains.keys():
                sql_string = f"{key_list[0]} like {placeholder_str}"
                values_list = [ f"%{val_val}%", ]
            if key_list[1] in sign_results_start_with.keys():
                sql_string = f"{key_list[0]} like {placeholder_str}"
                values_list = [ f"{val_val}%", ]
            if key_list[1] in sign_results_end_with.keys():
                sql_string = f"{key_list[0]} like {placeholder_str}"
                values_list = [ f"%{val_val}", ]

        return { 'sql_str': sql_string, 'values_list': values_list }

    def convert_handle(self, **kwargs):
        # 转换操作
        all_sql = ''
        for k in kwargs.keys():
            current_sql = self.key_convert_sql_result(k, kwargs[k])
            if all_sql > 1:
                all_sql = f"{all_sql} AND {current_sql}"
            else:
                all_sql = current_sql
        return all_sql

    def dict_convert_query_where_string(self, db_type_key, **kwargs):
        # 字典转换查询条件字符串
        use_placeholder_str = self.sql_placeholder_str(db_type_key)  # 占位符
        query_values_list = []         # 查询值
        where_string = ''

        if kwargs:
            for k in kwargs.keys():
                current_sql_dict = self.key_convert_sql_result(k, kwargs[k], use_placeholder_str)
                current_sql = current_sql_dict.get('sql_str', '')
                query_values_list.extend(current_sql_dict.get('values_list', []))

                if current_sql == '':
                    continue

                if len(where_string) > 1:
                    where_string = f"{where_string} AND ({current_sql})"
                else:
                    where_string = f"({current_sql})"
        return { 'where_str': where_string, 'values_tuple': tuple(query_values_list) }

    def dict_convert_instance_insert_class(self, table_class, **kwargs):
        # 字典实例化为插入类
        table_class_instance = table_class()
        for k in kwargs.keys():
            if hasattr(table_class_instance, k):
                setattr(table_class_instance, k, kwargs[k])
        return table_class_instance

    def dict_convert_insert_str(self, db_type_key, **kw):
        # 根据字典创建 列和值 的插入数据库字符串
        use_placeholder_str = self.sql_placeholder_str(db_type_key)  # 占位符

        insert_columns_str = ''         # 插入的列
        placeholders_str = ''           # 占位符
        insert_values_list = []         # 插入值

        for key in kw:
            current_insert_val = kw[key]
            # if isinstance(current_insert_val, str):
            #     current_insert_val = f"\"{current_insert_val}\""
            insert_columns_str = f"{insert_columns_str}, \"{key}\""
            placeholders_str = f"{placeholders_str}, {use_placeholder_str}"
            insert_values_list.append(current_insert_val)

        return {
            'columns': insert_columns_str.strip(', '),
            'placeholders': placeholders_str.strip(' ,'),
            'values_tuple': tuple(insert_values_list),
        }

    def dict_convert_update_str(self, db_type_key, **kw):
        # dict -> update str
        use_placeholder_str = self.sql_placeholder_str(db_type_key)  # 占位符
        update_values_list = []
        update_str = ''
        for k in kw.keys():
            update_str = f"{update_str}, {k}={use_placeholder_str}"
            update_values_list.append(kw[k])
        return {
            'update_str': update_str.strip(', '),
            'values_tuple': tuple(update_values_list),
        }

# if __name__ == '__main__':
#     text_string = 'test'
#     split_result = text_string.split('__', 1)
#     print(split_result)

#     round_test_dict = {'aa': 'isA', 'bb': 'isB'}
#     for k in round_test_dict.keys():
#         print(f"key is {k}, Value is {round_test_dict[k]}")
