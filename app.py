from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from apscheduler.schedulers.background import BackgroundScheduler



db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("src.config.config.Config")
    app.config['FLASK_ENV'] = 'production'
    app.config['DEBUG'] = False
    app.config['USE_RELOADER'] = False

    from src.models.product import Product
    from src.models.price import Price

    db.init_app(app)
    migrate.init_app(app, db)

    # register routes
    from src.config.routes import main_page
    app.register_blueprint(main_page)
    
    def scrap_page():
        with app.app_context():
            from src.utils.scrap_job import ScrapJob
            
            # print("Start scrap job")
            scrap = ScrapJob()
            scrap.check()
            # print("End scrap job")
    
    
    # running scheduler scrap page
    scheduler = BackgroundScheduler()

    scheduler.add_job(scrap_page, trigger='cron', hour="*")
    scheduler.start()


    # configure flask script manager
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.add_command('runserver', Server(host="0.0.0.0", port=5000))

    return manager.run()


if __name__ == "__main__":
    create_app()