import os
#
env_config = {}
def load_env_file(filepath):
  with open(filepath, 'r') as file:
    for line in file:
      # 忽略注释和空行
      if line.startswith('#') or not line.strip():
        continue
      # 拆分键和值，并去掉左右的空白字符
      key, value = line.strip().split('=', 1)
      env_config[key] = value
#
# 指定 .env 文件的路径
env_file_path = '.env'
load_env_file(env_file_path)

root_folder = os.getcwd()
rss_news_table_name_prefix = "z_rss_t_"

