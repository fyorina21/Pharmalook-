from app import create_app
from app import db
from app.database import Pharmacist


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

