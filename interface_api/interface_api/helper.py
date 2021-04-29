from interface_api import db, create_app

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

from interface_api.models import Heat, Match

match = Match(name_team_home = 'test_team_home', name_team_away = 'test_team_away', score_team_home=1, score_team_away=2)
db.session.add(match)
db.session.commit()

match2 = Match(name_team_home = 'test_team_home', name_team_away = 'test_team_away', score_team_home=3, score_team_away=4)
db.session.add(match2)
db.session.commit()

match3 = Match(**{'name_team_home': 'test_team_home', 'name_team_away': 'test_team_away', 'score_team_home':3, 'score_team_away':5})
db.session.add(match3)
db.session.commit()

heat = Heat(heat_id=1, match_id=1, heat_number=1, a_rider="test_rider", a_score=1, b_rider='test_rider', b_score=2, c_rider='test_rider', c_score=0, d_rider='test', d_score=2)
db.session.add(heat)
db.session.commit()

matches = Match.query.all()

match.serialize()
match.serialize(excl_list=['heats'])

heat = Heat.query.get(1)

