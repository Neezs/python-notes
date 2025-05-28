from flask import Flask, g
import pymysql

def create_app():
    app = Flask(__name__)

    app.config['DB_HOST'] = 'localhost'
    app.config['DB_USER'] = 'root'
    app.config['DB_PASSWORD'] = 'root'
    app.config['DB_NAME'] = 'ferreira_guilherme_deva1a_notes_2025'
    app.secret_key = 'your-secret-key'  #flash()

    def connect_db():
        return pymysql.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor
        )

    @app.before_request
    def before_request():
        g.db = connect_db()
        g.cursor = g.db.cursor()

    @app.teardown_request
    def teardown_request(exception):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()

    from .routes import menu, apprentice, branch, trainer, grade
    app.register_blueprint(menu.bp)
    app.register_blueprint(apprentice.bp)
    app.register_blueprint(branch.bp)
    app.register_blueprint(trainer.bp)
    app.register_blueprint(grade.bp)

    return app
