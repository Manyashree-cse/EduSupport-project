from flask import Flask

from config import Config
from extensions import db, login_manager


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Import routes
    from routes.auth import auth
    from routes.student import student
    from routes.staff import staff
    from routes.admin import admin

    # Register routes
    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(staff)
    app.register_blueprint(admin)

    # Create database tables
    with app.app_context():

        from models.user import User
        from models.ticket import Ticket
        from models.comment import Comment
        from models.activity import Activity
        from models.category import Category

        db.create_all()

        # Create default categories
        if Category.query.count() == 0:

            categories = [
                "Fees",
                "Attendance",
                "ID Card",
                "Certificates",
                "Documents",
                "General"
            ]

            for name in categories:
                db.session.add(Category(name=name))

            db.session.commit()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)