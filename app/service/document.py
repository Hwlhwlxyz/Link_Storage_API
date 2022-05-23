import json

from sqlalchemy import func
from sqlalchemy.sql import select

from app.model.document import Document
from app.model.tag import Tag
from app.model.user import User


def db_result_to_list(result):
    return [{"description": d.description, "url": d.url, "title": d.title, "id": d.id} for d in result]


def get_all_documents(session, userid):
    documents = session.query(Document).filter(Document.user_id == userid)
    return db_result_to_list(documents)


def get_all_documents_with_tags(session, userid):
    def transfer_result(query_doc_with_tag):
        tag_name_list = None
        tag_id_list = None
        document = query_doc_with_tag[0]
        if query_doc_with_tag[1] is not None:
            tag_name_list = query_doc_with_tag[1].split(',')
        if query_doc_with_tag[2] is not None:
            tag_id_list = query_doc_with_tag[2].split(',')
        tag_list = []
        if tag_name_list is not None and tag_id_list is not None:
            for (id, name) in zip(tag_id_list, tag_name_list):
                tag_list.append({'id':id, 'name':name})
        return {
            'id': document.id,
            'url': document.url,
            'description': document.description,
            'title': document.title,
            'tagNameList': tag_name_list,
            'tagIdList': tag_id_list,
            'tagList': tag_list
        }
    # https://stackoverflow.com/questions/26583832/sqlalchemy-group-concat-and-duplicates
    query = session.query(
        Document,
        func.group_concat(Tag.name),
        func.group_concat(Tag.id)
    ).join(Tag, Document.id == Tag.document_id, isouter=True).filter(Document.user_id == userid).group_by(Document.id)
    print(query)
    for q in query:
        print(transfer_result(q))
    return [transfer_result(q) for q in query]

def get_documents_with_tags_by_tag(session, userid, tag):
    def transfer_result(query_doc_with_tag):
        tag_name_list = None
        tag_id_list = None
        document = query_doc_with_tag[0]
        if query_doc_with_tag[1] is not None:
            tag_name_list = query_doc_with_tag[1].split(',')
        if query_doc_with_tag[2] is not None:
            tag_id_list = query_doc_with_tag[2].split(',')
        tag_list = []
        if tag_name_list is not None and tag_id_list is not None:
            for (id, name) in zip(tag_id_list, tag_name_list):
                tag_list.append({'id':id, 'name':name})
        return {
            'id': document.id,
            'url': document.url,
            'description': document.description,
            'title': document.title,
            'tagNameList': tag_name_list,
            'tagIdList': tag_id_list,
            'tagList': tag_list
        }
    # https://stackoverflow.com/questions/26583832/sqlalchemy-group-concat-and-duplicates
    query = session.query(
        Document,
        func.group_concat(Tag.name),
        func.group_concat(Tag.id)
    ).join(Tag, Document.id == Tag.document_id, isouter=True).\
        filter((Document.user_id == userid), (Tag.name == tag))\
        .group_by(Document.id)
    print(query)
    for q in query:
        print(transfer_result(q))
    return [transfer_result(q) for q in query]

def search_documents(session, userid, keyword):
    documents = session.query(Document).filter(Document.user_id == userid,
                                               Document.description.like('%' + keyword + '%'))
    return db_result_to_list(documents)


def add_document(session, userid, title, url, description):
    new_document = Document()
    new_document.user_id = userid
    new_document.title = title
    new_document.description = description
    new_document.url = url
    session.add(new_document)
    session.commit()
    return new_document


def update_document(session, userid, id, title, url, description):
    # TODO check userid

    current_doc = session.query(Document).filter(Document.id == id).one()
    current_doc.title = title
    current_doc.url = url
    current_doc.description = description
    session.commit()
    return current_doc


def delete_document(session, userid, id):
    # TODO check userid
    obj_to_delete = session.query(Document).filter(Document.id == id).one()
    session.delete(obj_to_delete)
    session.commit()
    return obj_to_delete
