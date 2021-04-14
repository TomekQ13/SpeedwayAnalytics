from interface_api import db, create_app

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

from interface_api.models import Heat, Match