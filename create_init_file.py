import sys
from pathlib import Path
import os
import copy

self_file_path = Path(__file__).resolve()
project_folder_path = str(self_file_path.parent.parent.parent)
sys.path.append(project_folder_path)

from common_classes.file_folder_handle import FileListConvert, TraversalFoldersFiles


class CreateInitFile(object):
    """
    创建 __init__.py file
    """
    def __init__(self) -> None:
        super().__init__()
        self.ignore_folders = ['ignore', '__pycache__', '.DS_Store', 'README.md', 'folder_tree.txt', 'create_nginx_docker_readme_files', 'auto_created_files', 'test_project']
        self.ignore_files = ['__init__.py', 'README.md', 'folder_tree.txt']
        self.file_list_convert_class = FileListConvert()
        self.traversal_folders_files_class = TraversalFoldersFiles()

    def path_connvert_python_from_import(self, path_str, replace_str=''):
        # 路径转换为 python 引用 字符串
        from_path = path_str.replace(replace_str, '')
        from_path = from_path.replace(os.path.sep, '.')
        from_path = from_path.strip('.py')
        return f"from {from_path} import *\n"

    def create_init_py_file(self):
        # 创建初始化文件 ~~~~~~~ 忽略的文件未添加 ignore_files ~~~~~~~
        # folders = self.traversal_folders_files_class.dir_names_in_folder(project_folder_path, *ignore_folders)
        files_paths = self.traversal_folders_files_class.file_paths_in_folder(str(self_file_path.parent), *self.ignore_folders)
        print(files_paths)
        split_text = copy.deepcopy(project_folder_path)
        line_list = []
        for f_path in files_paths:
            if Path(f_path).name in self.ignore_files:      # 忽略的文件
                continue
            current_line = self.path_connvert_python_from_import(str(Path('common_classes', 'zw_libs', f_path)), split_text)
            # print(current_line)
            line_list.append(current_line)
        init_py_file_path = str(Path(self_file_path.parent, '__init__.py'))
        self.file_list_convert_class.list_write_file(init_py_file_path, *line_list)


if __name__ == '__main__':
    # 操作 创建 __init__.py file
    create_init_file_class = CreateInitFile()
    create_init_file_class.create_init_py_file()
