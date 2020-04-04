
from . import db
from .models import Activity


def activity_like(act_id):
    act = Activity.query.get(act_id)

    if act is None:
        return False

    act.score = act.score+1
    db.session.add(act)
    db.session.commit()
    return True
