from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from sqlalchemy.schema import UniqueConstraint
db = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = f"sqlite:///main.db"


class Case(db.Model):
    __tablename__ = 'case'
    
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.Integer, nullable=False)
    case_year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(200))
    filing_date = db.Column(db.Date)
    next_date = db.Column(db.Date)
    last_date = db.Column(db.Date)
    petitioner = db.Column(db.String(500))
    respondent = db.Column(db.String(500))
    order_link = db.Column(db.Text)
    order_id = db.Column(db.Integer, unique=True)

    order = db.relationship('Order', backref='case_ref', uselist=False)
    
    def __repr__(self):
        return f'<Case {self.case_type}/{self.case_number}/{self.case_year}>'

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('case.order_id'), nullable=False)
    order_links = db.Column(db.JSON)
    
    def __repr__(self):
        return f'<Order {self.order_id}>'


