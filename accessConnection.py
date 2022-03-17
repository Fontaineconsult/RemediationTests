import os.path
from urllib.parse import quote_plus
from sqlalchemy import create_engine, Integer, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
Base = declarative_base()
from datetime import datetime

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_hash = Column(String(50))
    file_name = Column(String(50))
    file_location = Column(String(50))
    file_type = Column(String(50))



class AbbyyServerJobs(Base):

    __tablename__ = 'abbyyServerJobs'
    id = Column(Integer, primary_key=True)
    jobId = Column(String(50))
    file_id = Column(Integer)
    state = Column(String(50))


class Videos(Base):

    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    media_type = Column(String(50))
    title = Column(String())
    source_url = Column(String())
    date_added = Column(DateTime, default=datetime.utcnow)


class Courses(Base):

    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(50))
    course_id = Column(String(50))
    ilearn_id = Column(String(50))
    semester = Column(String(50))



print(os.path.isfile(r"C:\\Users\\913678186\\IdeaProjects\\RemediationTests\\ACRS.accdb"))

connection_string = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\913678186\IdeaProjects\RemediationTests\ACRS.accdb;"
    r"ExtendedAnsiSQL=1;")
connection_uri = f"access+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
engine = create_engine(connection_uri)



def get_session():

    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()



