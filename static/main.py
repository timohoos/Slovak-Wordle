from flask import Flask, Blueprint, jsonify
from sqlalchemy import create_engine
import os.path
import toml


bp = Blueprint('new-game', __name__)

@bp.route("/new-game", methods=['POST'])
def new_game():
    dummy_sid = '84984416189'

    with db.connect() as connection:
        word = connection.execute("select * from words order by random() limit 1").fetchall()[0][1]
        if (connection.execute("select count(*) from games WHERE session_id = %s", [dummy_sid,]).fetchall()[0][0]) > 0:
            connection.execute("update games set word = %s, guesses = %s where session_id = %s", (word, [], dummy_sid))
        else:
            connection.execute("insert into games (session_id, word, guesses) values(%s, %s, %s)", (dummy_sid, word, []))
    return jsonify({"state": "started"})


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app


settings = (toml.load(os.path.dirname(__file__) + "/../settings.toml"))
db_string = f"postgresql+psycopg2://{settings['database']['user']}:{settings['database']['password']}@{settings['database']['host']}:{settings['database']['port']}/{settings['database']['database']}"
db = create_engine(db_string, pool_size=20)

app = create_app()
