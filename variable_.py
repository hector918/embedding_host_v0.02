import os

def load_env_file(filepath):
  with open(filepath, 'r') as file:
    for line in file:
        # 忽略注释和空行
        if line.startswith('#') or not line.strip():
          continue
        # 拆分键和值，并去掉左右的空白字符
        key, value = line.strip().split('=', 1)
        os.environ[key] = value

# 指定 .env 文件的路径
env_file_path = '.env'
load_env_file(env_file_path)

# 访问环境变量
api_key = os.getenv('DEBUG')
