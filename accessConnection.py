import os.path
from urllib.parse import quote_plus
from sqlalchemy import create_engine, Integer, Column, String, DateTime, Boolean, ForeignKey
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
    origin_requester_id = Column(Integer())



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
    origin_requester_id = Column(Integer())



class CourseAssignments(Base):

    __tablename__ = 'course_assignments'
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(9))
    course_id = Column(Integer())


class Courses(Base):

    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(50))
    course_id = Column(String(50))
    ilearn_id = Column(String(50))
    semester = Column(String(50))

class CampusAssociation(Base):

    __tablename__ = 'campus_association'
    id = Column(Integer, primary_key=True)
    campus_org_id = Column(Integer)
    employee_id = Column(String(9))


class Employee(Base):

    __tablename__ = 'employee'
    employee_id = Column(String(9), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    email = Column(String())

class Orgs(Base):

    __tablename__ = 'orgs'
    id = Column(Integer, primary_key=True)
    org_name = Column(String())
    org_contact = Column(String())
    org_email = Column(String())

class ConversionRequester(Base):

    __tablename__ = 'conversion_requester'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer())
    campus_association_id = Column(Integer())

class VideoConversions(Base):

    __tablename__ = 'video_conversions'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer())
    conversion_req_id = Column(Integer())


class FileConversions(Base):

    __tablename__ = 'file_conversions'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer(), ForeignKey("files.id"))
    source_hierarchy = Column(String())
    conversion_req_id = Column(Integer(), ForeignKey("conversion_requests.id"))
    project_dir = Column(String())
    file_type = Column(String())

class ConversionRequests(Base):

    __tablename__ = 'conversion_requests'
    id = Column(Integer, primary_key=True)
    conversion_requester = Column(Integer())
    comments = Column(String())
    files_imported = Column(Boolean())

class PDFMetadata(Base):

    __tablename__ = 'pdf_metadata'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer())
    is_tagged = Column(Boolean())
    text_type = Column(Integer())
    total_figures = Column(Integer())
    total_alt_tags = Column(Integer())
    has_doc_desc = Column(Boolean())
    stage_folder = Column(String())
    title_set = Column(Boolean())
    lang_set = Column(Boolean())

class PDFMetadataAssignments(Base):

    __tablename__ = 'pdf_metadata_assignment'
    id = Column(Integer, primary_key=True)
    source_file_id = Column(Integer())
    conversion_file_id = Column(Integer())
    metadata_id = Column(Integer())



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



