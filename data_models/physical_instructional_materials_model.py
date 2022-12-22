from sqlalchemy import Integer, Column, ForeignKey, String
from base import Base




class CourseReadersAssignment(Base):

    __tablename__ = 'course_readers_assignment'
    id = Column(Integer(), primary_key=True)
    course_id = Column(Integer(),  ForeignKey("courses.id"))
    textbook_id = Column(Integer(),  ForeignKey("textbooks.id"))
    reader_id = Column(Integer(),  ForeignKey("readers.id"))
    file_id = Column(Integer(), ForeignKey("files.id"))

class Textbooks(Base):

    __tablename__ = 'textbooks'

    id = Column(Integer(), primary_key=True)
    isbn13 = Column(Integer())
    isbn10 = Column(Integer())
    title = Column(String())


class Readers(Base):

    __tablename__ = 'readers'
    id = Column(Integer(), primary_key=True)
    title = Column(String())



class TextbookImport(Base):

    __tablename__ = 'textbook_import'
    id = Column(Integer(), primary_key=True)
    title = Column(String())