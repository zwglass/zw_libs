from pathlib import Path
import subprocess

current_zw_libs_folder_path = str(Path(__file__).resolve().parent.parent)
zw_libs_path = '/Users/zhaoshenghua/development/programs/tools_projects/zw_libs'

def cmd(command):
    subprocess.run(command, shell=True)

def push_to_zw_libs():
    # 推送到 zw_libs_path
    async_command = f"rsync -av {current_zw_libs_folder_path}/  {zw_libs_path}"
    cmd(async_command)
    async_command = f"rsync -av {zw_libs_path}/  {current_zw_libs_folder_path}"
    cmd(async_command)

if __name__ == '__main__':
    push_to_zw_libs()
