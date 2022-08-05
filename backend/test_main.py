from main import create_app
import pytest
import os.path
import toml
import json


@pytest.fixture()
def app():
    settings = (toml.load(os.path.dirname(__file__) + "/../settings-test.toml"))
    app = create_app(settings)
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_new_game(app, client):
    with app.db.connect() as connection:
        connection.execute("truncate table games")
        connection.execute("truncate table words")
        connection.execute("insert into words (word) values (%s)", "srnka")
        response = client.post("/new-game")
        assert response.status_code == 200
        assert response.json["state"] == "started"
        assert connection.execute("select word from games").fetchall()[0]["word"] == "srnka"


def test_guess(app, client):
    with app.db.connect() as connection:
        connection.execute("truncate table words")
        connection.execute("insert into words (word) values (%s)", "srnka")
        response = client.post("/guess", data=json.dumps({"guess": "srnka"}), content_type="application/json")
        assert response.status_code == 200
        assert response.json["status"] == "ok"
