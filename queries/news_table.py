from datetime import datetime, timedelta
from db_config.source_db import source_db
from variable_ import rss_news_table_name_prefix
import inspect
#
def logging(e):
  debug_stack = ""
  for i in range(1, 4):  # 假设要追溯3层
    frame = inspect.stack()[i]
    debug_stack += f"{frame.filename}, {frame.lineno}; \n"
  print(e, debug_stack)
#
def read_news_rows(columns = ["hash_code", "title", "key_infomation", "table_name"], limit = 1000, period = None):
  #时段约束
  if period is None or not (isinstance(period["start_date"], datetime) and isinstance(period["end_date"], datetime)):
    period = {"start_date": datetime.now() - timedelta(days=365), "end_date": datetime.now()}
    
  #possible column name
  valid_columns = {"hash_code", "title", "key_infomation", "table_name", "origin_url", "create_at",  "embedding_is_created", "attempt_create_embedding", "publish_datetime"}
  columns = [col for col in columns if col in valid_columns]
  if not isinstance(limit, int): raise TypeError(f"Expected limit as an integer, but got {type(limit).__name__} instead.")

  # 替换表名,如果存在的话
  columns = ["tableoid::regclass AS table_name" if field == "table_name" else field for field in columns]

  news_tables_name = source_db.fetch_results(f"""SELECT CONCAT('{rss_news_table_name_prefix}', name) AS name FROM source_list WHERE status = 0;""")
  
  try:
    sub_query = []
    for tablename in news_tables_name:
      table_name_safe = tablename[0].replace('"', '""') 
      sub_query.append(f"""
        SELECT *
        FROM (
          SELECT {",".join(columns)}
          FROM {table_name_safe} 
          WHERE key_infomation_is_created = TRUE 
            AND publish_datetime BETWEEN %(start_date)s AND %(end_date)s
          LIMIT {limit}
        ) AS {table_name_safe}_results
      """)
    #
    query = f"""
      SELECT *
      FROM (
        {"UNION ALL".join(sub_query)}
      ) AS combined_results
      LIMIT {limit};
    """
    
    rows = source_db.fetch_results(query, period)
    return rows
  except Exception as e:
    logging(e)
    return []

def read_news_row_by_hashlist(hash_list, columns=["hash_code", "title", "key_infomation", "table_name"]):
  if not hash_list: return []

  valid_columns = {"hash_code", "title", "key_infomation", "table_name", "origin_url", "create_at", "embedding_is_created", "attempt_create_embedding", "publish_datetime"}
  columns = [col for col in columns if col in valid_columns]

  # Replace table_name with tableoid::regclass if it exists
  columns = ["tableoid::regclass AS table_name" if field == "table_name" else field for field in columns]

  news_tables_name = source_db.fetch_results(f"""SELECT CONCAT('{rss_news_table_name_prefix}', name) AS name FROM source_list WHERE status = 0;""")
  
  try:
    sub_query = []
    for tablename in news_tables_name:
      table_name_safe = tablename[0].replace('"', '""') 
      sub_query.append(f"""
        SELECT {",".join(columns)}
        FROM "{table_name_safe}" 
        WHERE hash_code = ANY(%(hash_list)s)
      """)
    
    query = f"""
      SELECT *
      FROM (
        {" UNION ALL ".join(sub_query)}
      ) AS combined_results;
    """
    
    rows = source_db.fetch_results(query, {"hash_list": hash_list})
    return rows
  except Exception as e:
    logging(e)
    return []

def read_html_files_by_hashlist():
  pass