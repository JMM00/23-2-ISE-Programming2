from app import db

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rent_date = db.Column(db.String(100), nullable=False)
    rent_place = db.Column(db.String(100), nullable=False)
    rent_time = db.Column(db.String(100), nullable=False)
    return_place = db.Column(db.String(100), nullable=False)
    return_time = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    login_id = db.Column(db.String(100), nullable=False)
    login_pw = db.Column(db.String(100), nullable=False)
