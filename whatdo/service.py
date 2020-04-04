
from . import app, db
from .models import Activity

def activity_like(id):
    act = Activity.query.get(id)
    
    if (act == None):
        return False

    act.score = act.score+1
    db.session.add(act)
    db.session.commit()