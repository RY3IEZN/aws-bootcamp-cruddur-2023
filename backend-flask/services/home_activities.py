from datetime import datetime, timedelta, timezone

from lib.db import db



class HomeActivities:
  def run(cognito_user_id = None):
    now = datetime.now(timezone.utc).astimezone()
  
    sql = db.template("home")
    results = db.query_array_json(sql)
    return results
   
