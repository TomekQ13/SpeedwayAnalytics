from interface_api import db, create_app

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

from interface_api.models import Heat, Match

match = Match(home_team = 'test_team_home', away_team = 'test_team_away', home_team_score=1, away_team_score=2)
db.session.add(match)
db.session.commit()

matches = Match.query.all()