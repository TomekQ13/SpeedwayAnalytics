from interface_api import db

class Heat(db.Model):
    __tablename__ = 'if_heat'
    heat_id = db.Column(db.Integer(), primary_key=True)
    match_id = db.Column(db.Integer(), db.ForeignKey('if_match.match_id', ondelete='CASCADE'))
    heat_number = db.Column(db.Integer(), nullable=False)
    a_rider = db.Column(db.String(64), nullable=False)
    a_score = db.Column(db.String(3), nullable=False)
    b_rider = db.Column(db.String(64), nullable=False)
    b_score = db.Column(db.String(3), nullable=False)
    c_rider = db.Column(db.String(64), nullable=False)
    c_score = db.Column(db.String(3), nullable=False)
    d_rider = db.Column(db.String(64), nullable=False)
    d_score = db.Column(db.String(3), nullable=False)

class Match(db.Model):
    __tablename__ = 'if_match'
    match_id = db.Column(db.Integer(), primary_key=True)
    home_team = db.Column(db.String(64))
    away_team = db.Column(db.String(64))
    home_team_score = db.Column(db.Integer())
    away_team_score = db.Column(db.Integer())
    heats = db.relationship('Heat', backref='match')