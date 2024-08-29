from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database


# con = "mysql+pymysql://root:kinl33giFT@18.138.11.189:3305/QR_DB_1"
# con = "mysql+pymysql://root:root@127.0.0.1:3306/DK_QR"


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = con
# db = SQLAlchemy(app)

# engine = create_engine(con, echo=True)
# if not database_exists(engine.url):
#     create_database(engine.url)
# else:
#     engine.connect()

from app.controller.ChatController import ChatController
