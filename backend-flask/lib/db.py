from psycopg_pool import ConnectionPool
import os

class Db:
  def __init__(self):
    self.init_pool()

  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)

# when we want to commit data to the db
  def query_commit():
    try:
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit
    except Exception as err:
      self.print_sql_err(err)
  
# when we want to get data to the db
  def query_array_json(self,sql):
    print("===datafrkm====")
    print(sql)
    print("===datafrkm====")
    wrapped_sql = self.query_wrap_array(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        print("===fromthedb===")
        json = cur.fetchone()
        print(json)
        print("===fromthedbs===")
        return json[0]

# when we want to get data to the db
  def query_object_json(self,sql):
    print("===datafrkm====")
    print(sql)
    print("===datafrkm====")
    wrapped_sql = self.query_wrap_object(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        print("===fromthedb==object=")
        json = cur.fetchone()
        print(json)
        print("===fromthedbs===")
        return json[0]
          
  def query_wrap_object(self,template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql

  def query_wrap_array(self,template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql



# error handleimg
  def print_sql_err(self,err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg ERROR:", err, "on line number:", line_num)
    print ("psycopg traceback:", traceback, "-- type:", err_type)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")




db = Db()