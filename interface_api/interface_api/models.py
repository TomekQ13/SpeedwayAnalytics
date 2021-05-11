from datetime import datetime
from enum import unique
from interface_api import db
from interface_api.utils import Serialize

class Heat(db.Model, Serialize):
    __tablename__ = 'if_heat'
    heat_id = db.Column(db.Integer(), primary_key=True)
    match_hash = db.Column(db.String(64), db.ForeignKey('if_match.match_hash', ondelete='CASCADE'))
    heat_number = db.Column(db.Integer(), nullable=False)
    a_rider = db.Column(db.String(64), nullable=False)
    a_score = db.Column(db.String(3), nullable=False)
    b_rider = db.Column(db.String(64), nullable=False)
    b_score = db.Column(db.String(3), nullable=False)
    c_rider = db.Column(db.String(64), nullable=False)
    c_score = db.Column(db.String(3), nullable=False)
    d_rider = db.Column(db.String(64), nullable=False)
    d_score = db.Column(db.String(3), nullable=False)
    added_dttm = db.Column(db.DateTime(), nullable=False, default=datetime.now)

class Match(db.Model, Serialize):
    __tablename__ = 'if_match'
    match_id = db.Column(db.Integer(), primary_key=True)
    match_hash = db.Column(db.String(64), nullable=False, index=True, unique=True)
    match_url = db.Column(db.Text(), nullable=False)
    stadium = db.Column(db.String(128), nullable=False)
    round = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    name_team_home = db.Column(db.String(64), nullable=False)
    name_team_away = db.Column(db.String(64), nullable=False)
    score_team_home = db.Column(db.Integer(), nullable=False)
    score_team_away = db.Column(db.Integer(), nullable=False)
    heats = db.relationship('Heat', backref='match')
    added_dttm = db.Column(db.DateTime(), nullable=False, default=datetime.now())



        