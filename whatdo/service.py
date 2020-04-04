
from . import db
from .models import Activity
from datetime import datetime

def activity_like(id):
    activity = Activity.query.get(id)
    
    if (activity == None):
        return False

    activity.likes += 1
    now = datetime.utcnow() # Db saves in UTC. Could be changed in settings.cfg

    incrementScore = calculate_score(activity.created,now)
    activity.score += incrementScore

    db.session.add(activity)
    db.session.commit()

    print("Added {:.2f} score to activity {} ".format(incrementScore,id,id))
    return True

def calculate_score(date, newerDate, weight=0.05):
    diff = newerDate - date
    duration_in_s = diff.total_seconds()
    duration_in_hours = int(duration_in_s/3600)

    if duration_in_hours == 0:
        return 1

    score = 1/(1+(duration_in_hours*weight))
    return score
