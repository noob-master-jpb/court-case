from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///main.db')

class Query(db.Model):
    __tablename__ = 'query'
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.Integer, nullable=False)
    case_year = db.Column(db.Integer, nullable=False)
    cases = db.relationship('Case', backref='query', lazy=True)
    def __repr__(self):
        return f'<Query {self.id}>'
class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'), nullable=False)
    case_type = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.Integer, nullable=False)
    case_year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(200))
    filing_date = db.Column(db.String(20))
    next_date = db.Column(db.String(20))
    last_date = db.Column(db.String(20))
    petitioner = db.Column(db.Text)
    respondent = db.Column(db.Text)
    order_link = db.Column(db.Text)
    orders = db.Column(db.JSON)    
    
    def __repr__(self):
        return f'<Case {self.case_type}/{self.case_number}/{self.case_year}>'






