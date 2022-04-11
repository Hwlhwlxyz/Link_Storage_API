from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .document import Document
from .user import User
from ..configuration.database import Base


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    document_id = Column(Integer, ForeignKey(Document.id))
    user_id = Column(Integer, ForeignKey(User.id))


