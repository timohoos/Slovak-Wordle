from flask import Flask, Blueprint, current_app, request
from sqlalchemy import create_engine
import os.path
import toml


bp = Blueprint("main", __name__, url_prefix="/")
dummy_sid = "84984416189"


@bp.post("/new-game")
def new_game():
    with current_app.db.connect() as connection:
        word = connection.execute("select * from words order by random() limit 1").fetchall()[0]["word"]
        if (connection.execute("select count(*) from games where session_id = %s", [dummy_sid,]).fetchall()[0][0]) > 0:
            connection.execute("update games set word = %s, guesses = %s where session_id = %s", (word, [], dummy_sid))
        else:
            connection.execute("insert into games (session_id, word, guesses) values(%s, %s, %s)", (dummy_sid, word, []))
    return {"state": "started"}


@bp.post("/guess")
def guess():
    with current_app.db.connect() as connection:

        guess = request.get_json()["guess"].lower()

        if (connection.execute("select count(*) from words where word = %s", [guess,]).fetchall()[0][0]) == 0:
            return {"status": "word not valid"}

        connection.execute("update games set guesses = array_append(guesses, %s) where session_id = %s", (guess, dummy_sid))
        guesses = connection.execute("select * from games where session_id = %s", [dummy_sid,]).fetchall()[0]["guesses"]

        #get game status here

        status = {"status": "ok"}

        return status


def create_app(settings=None):
    app = Flask(__name__)
    app.register_blueprint(bp)
    if settings is None:
        settings = (toml.load(os.path.dirname(__file__) + "/../settings.toml"))
    db_string = f"postgresql+psycopg2://{settings['database']['user']}:{settings['database']['password']}@{settings['database']['host']}:{settings['database']['port']}/{settings['database']['database']}"
    app.db = create_engine(db_string, pool_size=20)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001)
