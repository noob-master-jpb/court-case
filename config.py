from app import app, db
from model import *
with app.app_context():
    db.create_all()