from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False, unique=True)
    password = db.Column(db.String,nullable=False)


    def get_id(self):
        return self.user_id


class Tracker(db.Model):
    __tablename__ = 'tracker'
    tracker_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False,unique=True)
    description = db.Column(db.String)
    type = db.Column(db.String,nullable=False)
    setting = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)



class Log(db.Model):
    __tablename__ = 'log'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.tracker_id", ondelete='CASCADE'))
    log_track = db.Column(db.String, nullable=False)
    note = db.Column(db.String)
    time = db.Column(db.String, nullable=False)

