
from datetime import datetime

from sqlalchemy import desc
from . import db
from .models import Activity


def activity_like(id):
    activity = Activity.query.get(id)

    if (activity is None):
        return False

    activity.likes += 1
    now = datetime.utcnow()  # Db saves in UTC. Could be changed in settings.cfg

    increment_score = calculate_score(activity.created, now)
    activity.score += increment_score

    db.session.add(activity)
    db.session.commit()

    print("Added {:.2f} score to activity {} ".format(increment_score, id))
    return True


def calculate_score(date, later_date, weight=0.05):
    diff = later_date - date
    duration_in_s = diff.total_seconds()
    duration_in_hours = int(duration_in_s/3600)

    if duration_in_hours == 0:
        return 1

    score = 1/(1+(duration_in_hours*weight))
    return score


def get_activities_ordered(excludeActivities):
    query = Activity.query.order_by(desc(Activity.score))
    if len(excludeActivities) > 0:
        query = query.filter(~Activity.id.in_(excludeActivities))

    activities = query.all()
    return activities

def activity_delete(id):
    activity = Activity.query.get(id)
    if (activity is None):
        return False
    db.session.delete(activity)
    db.session.commit()
    return True
