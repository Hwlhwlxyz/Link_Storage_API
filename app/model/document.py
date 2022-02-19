from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .user import User
from ..configuration.database import Base


class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User", back_populates="document")

    type = Column(String)

    # type=link
    url = Column(String)
    description = Column(String)


