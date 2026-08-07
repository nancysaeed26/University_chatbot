import pymysql
import os

db = pymysql.connect(
    host=os.getenv("MYSQLHOST", "shinkansen.proxy.rlwy.net"),
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD", "vDwUbLnBYslzghjJAHVBlJWyDxTpiGYc"),
    database=os.getenv("MYSQLDATABASE", "railway"),
    port=int(os.getenv("MYSQLPORT", 57455)),
    charset="utf8mb4"
)