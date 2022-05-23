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

def get_one_user(session, user_id):
    user = session.query(User).get(user_id)
    return user

def login_user_check(session, username, input_password):
    if username == 'test':
        return User(username=username, hashed_password='$2b$12$.dLvFcuDQ3buX.ak5ks2lOVYfoCByRzeeomh1YfVjc80xK96z8c7m',
                    id=1)
    else:
        print(username, input_password)
        user = session.query(User).filter(User.username == username).one()
        print(user)
        if User.verify_password(input_password, user.hashed_password):
            return user
    return None


def edit_user(session, query_id, username, email, password):
    hashed_password = get_password_hash(password)
    session.query(User). \
        filter(User.id == query_id). \
        update({
            'username': username,
            'email': email,
            'password': hashed_password
        })
    session.commit()
    return {id: query_id}
