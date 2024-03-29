from psycopg_pool import ConnectionPool
import os
import re
import sys
from flask import current_app as app

class Db:
  def __init__(self):
    self.init_pool()


  def template(self,*args):
    pathing = list((app.root_path,'db','sql',) + args)
    pathing[-1] = pathing[-1] + ".sql"

    template_path = os.path.join(*pathing)


    with open(template_path, 'r') as f:
      template_content = f.read()
    return template_content  

  def init_pool(self):
    # connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool("postgres://postgres:postgres123#@cruddur-db-instance.chupgxpbfimi.eu-west-2.rds.amazonaws.com:5432/cruddur")

  def print_sql(self,title,sql,params={}):
    cyan = '\033[96m'
    no_color = '\033[0m'
    print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
    print(sql,params)

# when we want to commit data to the db
  def query_commit_with_id(self,sql,params={}):
    print("----SQLSTATEMENT----")
    print(sql)
    print("----SQLSTATEMENT----")
    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)

    try:
      with self.pool.connection()as conn:
        cur = conn.cursor()
        cur.execute(sql,params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit
        if is_returning_id:
          return returning_id
    except Exception as err:
      self.print_sql_err(err)

  
# when we want to get data to the db
  def query_array_json(self,sql,params={}):
    print("===datafrkm====")
    print(sql)
    print("===datafrkm====")
    wrapped_sql = self.query_wrap_array(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        print("===fromthedb===")
        json = cur.fetchone()
        print(json)
        print("===fromthedbs===")
        return json[0]

# when we want to get data to the db
  def query_object_json(self,sql,params):
    print("===datafrkm====")
    print(sql)
    print("===datafrkm====")
    wrapped_sql = self.query_wrap_object(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        print("===fromthedb==object=")
        json = cur.fetchone()
        if json == None:
          "{}"
        else:
          return json[0]
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

  def query_value(self,sql,params={}):
    self.print_sql('value',sql,params)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql,params)
        json = cur.fetchone()
        return json[0]



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