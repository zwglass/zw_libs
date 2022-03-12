from pathlib import Path
import subprocess

# 拉取 zw_libs 文件夹下的所有文件 同步到本地

current_zw_libs_folder_path = str(Path(__file__).resolve().parent.parent)
zw_libs_path = '/Users/zhaoshenghua/development/programs/tools_projects/zw_libs'

def cmd(command):
    subprocess.run(command, shell=True)

def pull_from_zw_libs():
    # 拉取 zw_libs
    async_command = f"rsync -av {zw_libs_path}/  {current_zw_libs_folder_path}"
    cmd(async_command)

if __name__ == '__main__':
    pull_from_zw_libs()

