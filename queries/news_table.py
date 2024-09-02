
def read_html_file_list_to_embedding():
  
  news_tables_name = source_db.fetch_results(f"""SELECT CONCAT('{rss_news_table_name_prefix}', name) AS name FROM source_list WHERE status = 0;""")

  column_template = { "hash_code": "hash_code", "origin_url": "origin_url", "title": "title", "key_infomation": "key_infomation", "create_at": "create_at", "embedding_is_created": "embedding_is_created", "attempt_create_embedding": "attempt_create_embedding", "publish_datetime": "publish_datetime", "table_name": "tableoid::regclass AS table_name"}
  try:
    result = []
    for tablename in news_tables_name:
      
      query = f"""
        UPDATE {tablename[0]} 
          SET attempt_create_embedding = attempt_create_embedding + 1
          WHERE id IN (
            SELECT id 
            FROM {tablename[0]} 
            WHERE 
              extract_from_source = true 
              AND key_infomation_is_created = true 
              AND embedding_is_created = false 
              AND attempt_create_embedding < 5 
            ORDER BY attempt_create_embedding ASC 
            LIMIT 5
          )
          RETURNING {",".join(column_template.values())};
      """
      rows = source_db.fetch_results(query)
      for row in rows:
        result.append(row)
    return {"column_template": column_template, "rows": result}
  except Exception as e:
    logging(e)
    return {"column_template": column_template, "rows": []}
