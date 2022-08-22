from time import sleep
from game import Game
from flask import Flask, Blueprint, current_app, request
from sqlalchemy import create_engine
import os.path
import toml
from flask_cors import CORS


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
    return {"status": "started"}


@bp.post("/get-game")
def get_game():
    with current_app.db.connect() as connection:
        data = connection.execute("select * from games where session_id = %s", [dummy_sid]).fetchall()
        word = ""
        if len(data) > 0:
            guesses, word = data[0]["guesses"], data[0]["word"]

            game = Game(word)
            game.add_guesses(guesses)

        else:
            game = Game(word)

        state = get_state(game, game.correct)
        if word == "":
            state["status"] = "waiting"
        return state


@bp.post("/guess")
def guess():
    with current_app.db.connect() as connection:
        guess = request.get_json()["guess"].casefold()
        data = connection.execute("select * from games where session_id = %s", [dummy_sid]).fetchall()
        guesses, word = data[0]["guesses"], data[0]["word"]

        game = Game(word)
        game.add_guesses(guesses)

        if (connection.execute("select count(*) from words where word = %s", [guess]).fetchall()[0][0]) == 0:
            return {**get_state(game), "status": "invalid word"}

        connection.execute("update games set guesses = array_append(guesses, %s) where session_id = %s", (guess, dummy_sid))

        game.add_guess(guess)
        return get_state(game)


def create_app(settings=None):
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000", "http://localhost:3001"], supports_credentials=True)
    app.register_blueprint(bp)
    if settings is None:
        settings = (toml.load(os.path.dirname(__file__) + "/../settings.toml"))
    db_string = f"postgresql+psycopg2://{settings['database']['user']}:{settings['database']['password']}@{settings['database']['host']}:{settings['database']['port']}/{settings['database']['database']}"
    app.db = create_engine(db_string, pool_size=20)
    return app


def get_state(game):

    if game.correct:
        status = "won"
    elif len(game.guesses_state) == Game.MAX_GUESSES:
        status = "lost"
    else:
        status = "ongoing"

    return {
        "status": status,
        "game": {
            "guesses": game.guesses_state,
            "overall_state": game.overall_state
        }
    }


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001)
