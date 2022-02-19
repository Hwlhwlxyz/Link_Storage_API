from app.model.document import Document


def get_all_documents(session, userid):
    documents = session.query(Document).filter(Document.user_id == userid)
    # for d in documents:
    #     print(d.description, d.url)
    return [{"description": d.description, "url": d.url} for d in documents]


def search_documents(session, userid, keyword):
    documents = session.query(Document).filter(Document.user_id == userid,
                                               Document.description.like('%' + keyword + '%'))
    return documents

def add_document(session, userid, url, description):
    new_document = Document()
    new_document.user_id = userid
    new_document.description = description
    new_document.url = url
    session.add(new_document)
    session.commit()
    return new_document


