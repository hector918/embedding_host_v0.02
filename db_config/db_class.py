import psycopg2
from psycopg2 import pool, OperationalError, Error
import threading
import time



class DatabaseConnectionPool:
  def __init__(self, dbname, user, password, host, port, sslmode='require', minconn=1, maxconn=10, max_retries=5, retry_delay=5):
    self.dbname = dbname
    self.user = user
    self.password = password
    self.host = host
    self.port = port
    self.sslmode = sslmode
    self.minconn = minconn
    self.maxconn = maxconn
    self.max_retries = max_retries
    self.retry_delay = retry_delay
    self.pool = None
    self.lock = threading.Lock()
    self._initialize_pool()

  def _initialize_pool(self):
    retries = 0
    while retries < self.max_retries:
      try:
        self.pool = psycopg2.pool.SimpleConnectionPool(
          self.minconn,
          self.maxconn,
          dbname=self.dbname,
          user=self.user,
          password=self.password,
          host=self.host,
          port=self.port,
          sslmode=self.sslmode
        )
        if self.pool:
          self.print("Connection pool created successfully.")
          return
      except OperationalError as e:
        self.print(f"An error occurred while creating the connection pool: {e}")
        retries += 1
        if retries < self.max_retries:
          self.print(f"Retrying in {self.retry_delay} seconds... ({retries}/{self.max_retries})")
          time.sleep(self.retry_delay)
        else:
          self.print("Max retries reached. Could not create the connection pool.")
          raise

  def ensure_connection(self, conn):
    try:
      if conn.closed:
        self.print("Connection lost. Reconnecting...")
        self._initialize_pool()
        return self.pool.getconn()
    except OperationalError as e:
      self.print(f"Failed to reconnect: {e}")
      raise
    return conn

  def get_connection(self):
    with self.lock:
      try:
        conn = self.pool.getconn()
        return self.ensure_connection(conn)
      except Error as e:
        self.print(f"An error occurred while getting a connection from the pool: {e}")
        raise

  def get_with_cursor(self):
    with self.lock:
      conn = None
      try:
        conn = self.pool.getconn()
        conn = self.ensure_connection(conn)
        conn.begin()
        try:
          with conn.cursor() as cursor:
            yield cursor
          conn.commit()
        except Error as cursor_error:
          conn.rollback()
          print(f"An error occurred while using the cursor: {cursor_error}")
          raise
        finally:
          self.release_connection(conn)
      except Error as conn_error:
        if conn:
          conn.rollback()
          self.release_connection(conn)
        print(f"An error occurred while getting a connection from the pool: {conn_error}")
        raise

  def release_connection(self, conn):
    with self.lock:
      try:
        self.pool.putconn(conn)
      except Error as e:
        self.print(f"An error occurred while releasing the connection: {e}")
        raise

  def close_all_connections(self):
    with self.lock:
      try:
        self.pool.closeall()
        self.print("All connections in the pool have been closed.")
      except Error as e:
        self.print(f"An error occurred while closing all connections: {e}")
        raise

  def execute_query(self, query, params=None):
    conn = self.get_connection()
    cursor = conn.cursor()
    try:
      cursor.execute(query, params)
      conn.commit()
      # self.print("Query executed successfully.")
    except Error as e:
      self.print(f"An error occurred while executing the query: {e}")
    finally:
      cursor.close()
      self.release_connection(conn)

  def execute_many_query(self, query, params=None):
    conn = self.get_connection()
    cursor = conn.cursor()
    try:
      cursor.executemany(query, params)
      conn.commit()
      # self.print("Query executed successfully.")
    except Error as e:
      self.print(f"An error occurred while executing the query: {e}")
    finally:
      cursor.close()
      self.release_connection(conn)

  def fetch_results(self, query, params=None):
    conn = self.get_connection()
    cursor = conn.cursor()
    try:
      cursor.execute(query, params)
      results = cursor.fetchall()
      return results
    except Error as e:
      self.print(f"An error occurred while fetching the results: {e}")
      return None
    finally:
      cursor.close()
      self.release_connection(conn)
  def print(self,any):
    print(f"{self.dbname} log: {any}")

