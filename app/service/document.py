from app.model.document import Document

def db_result_to_list(result):
    return [{"description": d.description, "url": d.url, "title": d.title} for d in result]

def get_all_documents(session, userid):
    documents = session.query(Document).filter(Document.user_id == userid)
    return db_result_to_list(documents)


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


