from app.configuration.database import get_db
from app.model.user import User, get_password_hash

def create_user(session, username, email, password):

    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    session.add(new_user)
    session.commit()
    return new_user

def get_all_users(session):
    users = session.query(User).all()
    return users
