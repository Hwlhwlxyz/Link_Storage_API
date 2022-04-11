from app.model.tag import Tag


def add_tag(session, userid, document_id, name):
    new_tag = Tag()
    new_tag.user_id = userid
    new_tag.document_id = document_id
    new_tag.name = name
    session.add(new_tag)
    session.commit()
    return new_tag

def update_tag_list(session, userid, document_id, name_list):

    return