from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def get_all_users():
    from app.models import User
    return User.query.all()

def get_user_by_email_or_mobile(email, mobile):
    from app.models import User
    user = User.query.filter((User.email == email) | (User.mobile == mobile)).first()
    return user is not None

def add_user(name, email, mobile, time_zone):
    from app.models import User
    user = User(name=name, email=email, mobile=mobile, timezone=time_zone)
    db.session.add(user)
    db.session.commit()
    return user

def get_users_not_replied():
    from app.models import User
    return User.query.filter_by(replied=False).all()

def set_replied(user_id):
    from app.models import User
    user = User.query.get(user_id)
    user.replied = True
    db.session.commit()
    return user