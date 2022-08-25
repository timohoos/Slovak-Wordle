from distutils.log import error
from game import Game
from flask import Flask, Blueprint, current_app, request, jsonify
from sqlalchemy import create_engine
import os.path
import toml
from uuid import uuid4
from flask_cors import CORS


bp = Blueprint("main", __name__, url_prefix="/")


@bp.post("/get-word")
def get_word():
    session_id = request.cookies.get("session_id")
    if not session_id:
        return ({"status": "400 Bad Request"}, 400)

    with current_app.db.connect() as connection:
        guesses, word = [], None

        games_rows = connection.execute("select * from games where session_id = %s", [session_id]).fetchall()
        if len(games_rows) == 0:
            return ({"status": "400 Bad Request"}, 400)

        guesses, word = games_rows[0]["guesses"], games_rows[0]["word"]
        game = Game(word)
        game.add_guesses(guesses)

        state = get_state(game)
        if state["status"] == "ongoing":
            return ({"status": "400 Bad Request"}, 400)

        return {"word": word}


@bp.post("/new-game")
def new_game():
    response = jsonify({"status": "started"})
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie("session_id", session_id)

    with current_app.db.connect() as connection:
        word = connection.execute("select * from words order by random() limit 1").fetchall()[0]["word"]
        if (connection.execute("select count(*) from games where session_id = %s", [session_id,]).fetchall()[0][0]) > 0:
            connection.execute("update games set word = %s, guesses = %s where session_id = %s", (word, [], session_id))
        else:
            connection.execute("insert into games (session_id, word, guesses) values(%s, %s, %s)", (session_id, word, []))
    return response


@bp.post("/get-game")
def get_game():
    with current_app.db.connect() as connection:
        guesses, word = [], None

        response = None
        session_id = request.cookies.get("session_id")
        if not session_id:
            word = connection.execute("select * from words order by random() limit 1").fetchall()[0]["word"]
            session_id = str(uuid4())
            response = jsonify(get_state(Game(word)))
            response.set_cookie("session_id", session_id)
            connection.execute("insert into games (session_id, word, guesses) values(%s, %s, %s)", (session_id, word, []))
        else:
            games_rows = connection.execute("select * from games where session_id = %s", [session_id]).fetchall()
            if len(games_rows) == 0:
                return ({"status": "400 Bad Request"}, 400)

            guesses, word = games_rows[0]["guesses"], games_rows[0]["word"]
            game = Game(word)
            game.add_guesses(guesses)
            response = get_state(game)

        return response


@bp.post("/guess")
def guess():
    with current_app.db.connect() as connection:
        session_id = request.cookies.get("session_id")

        if not session_id:
            return ({"status": "400 Bad Request"}, 400)

        guess = request.get_json()["guess"].casefold()
        games_rows = connection.execute("select * from games where session_id = %s", [session_id]).fetchall()
        guesses, word = games_rows[0]["guesses"], games_rows[0]["word"]

        game = Game(word)
        game.add_guesses(guesses)

        if (connection.execute("select count(*) from words where word = %s", [guess]).fetchall()[0][0]) == 0:
            return {**get_state(game), "status": "invalid word"}

        connection.execute("update games set guesses = array_append(guesses, %s) where session_id = %s", (guess, session_id))

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
