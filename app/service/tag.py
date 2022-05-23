from app.model.tag import Tag


def add_tag(session, userid, document_id, name):
    new_tag = Tag()
    new_tag.user_id = userid
    new_tag.document_id = document_id
    new_tag.name = name
    session.add(new_tag)
    session.commit()
    return new_tag

def add_tag_list(session, userid, document_id, name_list):
    exist_tag_list = get_tag_list(session, userid, document_id)
    exist_tag_name_list = [t.name for t in exist_tag_list]
    tags_to_insert = []
    for n in name_list:
        if n not in exist_tag_name_list:
            new_tag = Tag()
            new_tag.user_id = userid
            new_tag.document_id = document_id
            new_tag.name = n
            tags_to_insert.append(new_tag)
    result = None
    # add
    if len(tags_to_insert) > 0:
        result = session.bulk_save_objects(tags_to_insert)
        session.commit()
    return result

def delete_tag_list(session, userid, document_id, name_list):
    exist_tag_list = get_tag_list(session, userid, document_id)
    tags_id_to_delete = []
    for e in exist_tag_list:
        if e.name in name_list:
            tags_id_to_delete.append(e.id)
    result = session.query(Tag).filter(Tag.id.in_(tags_id_to_delete)).delete()
    session.commit()
    return result

def update_tag_list(session, userid, document_id, name_list):
    exist_tag_list = get_tag_list(session, userid, document_id)
    exist_tag_name_list = [t.name for t in exist_tag_list]
    names_to_add = list(set(name_list) - set(exist_tag_name_list))
    names_to_delete = list(set(exist_tag_name_list) - set(name_list))
    add = add_tag_list(session, userid, document_id, names_to_add)
    delete = delete_tag_list(session, userid, document_id, names_to_delete)
    return {'add': add, 'delete': delete}


def get_tag_list(session, userid, document_id):
    tag_list = session.query(Tag).filter(
        Tag.user_id==userid,
        Tag.document_id==document_id
    ).all()
    return tag_list

