import os

#root_folder = os.getcwd()
root_folder = "/home/ym2380/news/embedding_host_v0.02"   ### Setting root folder instead
rss_news_table_name_prefix = "z_rss_t_"

env_config = {}
def load_env_file(filepath):
  with open(filepath, 'r') as file:
    for line in file:
      if line.startswith('#') or not line.strip():
        continue
      key, value = line.strip().split('=', 1)
      env_config[key] = value

env_file_path = os.path.join(root_folder, ".env")
load_env_file(env_file_path)