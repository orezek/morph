import os

# Root project and upload directory location
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "app/static", "uploaded_files")

# TODO: Change the secrets into environmental variables or use AWS parameter store etc.
# DB engine and connection setup - make ENV or AWS Param. store
user_name = "admin"
password = "Mirodinga1"
db_engine_driver = "mysql+pymysql"
db_url = "aurora-app-prod.ccj4auatnl5l.eu-central-1.rds.amazonaws.com"
db_port = "3306"
db_name = "aurora"
db_charset = "charset=utf8mb4"
# SQLite DB connection for local testing
db_connection_sqlite = "sqlite:///" + os.path.join(APP_ROOT, "app/data.sqlite")
# MariaDB's connection for AWS RDS database
db_connection_mariadb = f"{db_engine_driver}://{user_name}:{password}@{db_url}:{db_port}/{db_name}?{db_charset}"


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "adfadfsfsfds"
    UPLOAD_FOLDER = UPLOAD_FOLDER
    SQLALCHEMY_DATABASE_URI = db_connection_mariadb
    DEBUG_TB_ENABLED = True
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = "5001"
