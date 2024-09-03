from db_config.db_class import DatabaseConnectionPool

from variable_ import env_config
logging = print
db_config = {
  'dbname': env_config['MAIN_DB_NAME'],
  'user': env_config['MAIN_DB_USER'],
  'password': env_config['MAIN_DB_PASSWORD'],
  'host': env_config['MAIN_DB_HOST'],
  'port': env_config['MAIN_DB_PORT'],
  'sslmode': 'require'
}

# Create a database connection instance
source_db = DatabaseConnectionPool(**db_config)


try:
  result = source_db.fetch_results(""" SELECT tablename 
  FROM pg_catalog.pg_tables   
  WHERE schemaname != 'information_schema' AND schemaname !=  'pg_catalog'  
  ORDER BY tablename; """)
  logging(f"log main table name: {result}")
except Exception as e:
  logging(f"An exception occurred on main db module: {str(e)}.")

# CREATE TABLE source_list (
#     id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     url text,
#     name text UNIQUE,
#     update_at timestamp with time zone,
#     status integer DEFAULT 0,
#     lastest_resp text
# );
