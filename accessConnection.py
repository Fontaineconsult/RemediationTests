
from sqlalchemy import create_engine, Integer, Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
Base = declarative_base()
from datetime import datetime

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_hash = Column(String())
    file_name = Column(String())
    file_location = Column(String())
    file_type = Column(String())
    origin_requester_id = Column(Integer(), ForeignKey("conversion_requester.id"))



class ConversionFilesAssignments(Base):

    __tablename__ = 'conversion_file_assignments'
    id = Column(Integer, primary_key=True)
    conversion_id = Column(Integer(),  ForeignKey("file_conversions.id"))
    file_id = Column(Integer(), ForeignKey("files.id"))
    stage = Column(String())




class BoxLocations(Base):

    __tablename__ = "box_locations"
    id = Column(Integer, primary_key=True)
    box_url = Column(String())
    owner = Column(String(), ForeignKey("employee.employee_id"))
    is_active = Column(Boolean())


class BoxAssociations(Base):

    __tablename__ = 'box_associations'
    id = Column(Integer, primary_key=True)
    box_id = Column(String(50))
    conversion_id = Column(String())

class AbbyyServerJobs(Base):

    __tablename__ = 'abbyyServerJobs'
    id = Column(Integer, primary_key=True)
    jobId = Column(String(50))
    file_id = Column(Integer, ForeignKey("files.id"))
    state = Column(String(50))


class Videos(Base):

    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    media_type = Column(String(50))
    title = Column(String())
    source_url = Column(String())
    date_added = Column(DateTime, default=datetime.utcnow)
    origin_requester_id = Column(Integer(), ForeignKey("conversion_requester.id"))



class CourseAssignments(Base):

    __tablename__ = 'course_assignments'
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(9),  ForeignKey("employee.employee_id"))
    course_id = Column(Integer(), ForeignKey("course.id"))


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
    campus_org_id = Column(Integer, ForeignKey("orgs.id"))
    employee_id = Column(String(9), ForeignKey("employee.employee_id"))


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
    course_id = Column(Integer(), ForeignKey("course.id"))
    campus_association_id = Column(Integer(), ForeignKey("campus_association.id"))

class VideoConversions(Base):

    __tablename__ = 'video_conversions'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer(), ForeignKey("videos.id"))
    conversion_req_id = Column(Integer(), ForeignKey("conversion_requests.id"))


class FileConversions(Base):

    __tablename__ = 'file_conversions'
    id = Column(Integer, primary_key=True)
    source_hierarchy = Column(String())
    conversion_req_id = Column(Integer(), ForeignKey("conversion_requests.id"))
    project_dir = Column(String())
    file_type = Column(String())

class ConversionRequests(Base):

    __tablename__ = 'conversion_requests'
    id = Column(Integer, primary_key=True)
    conversion_requester = Column(Integer(), ForeignKey("conversion_requester.id"))
    comments = Column(String())
    files_imported = Column(Boolean())
    import_folder = Column(String())




class PDFMetadata(Base):

    __tablename__ = 'pdf_metadata'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer(), ForeignKey("files.id"))
    is_tagged = Column(Boolean())
    text_type = Column(Integer())
    total_figures = Column(Integer())
    total_alt_tags = Column(Integer())
    has_doc_desc = Column(Boolean())
    stage_folder = Column(String())
    title_set = Column(Boolean())
    lang_set = Column(Boolean())
    number_of_pages = Column(Integer())

class PDFMetadataAssignments(Base):

    __tablename__ = 'pdf_metadata_assignment'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer(), ForeignKey("files.id"))
    metadata_id = Column(Integer(), ForeignKey("pdf_metadata.id"))



#
# print(os.path.isfile(r"C:\\Users\\913678186\\IdeaProjects\\RemediationTests\\ACRS.accdb"))
#
# connection_string = (
#     r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
#     r"DBQ=C:\Users\913678186\IdeaProjects\RemediationTests\ACRS.accdb;"
#     r"ExtendedAnsiSQL=1;")
# connection_uri = f"access+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
# engine = create_engine(connection_uri)


psql_connection = "postgresql://postgres:accesslearning!1@130.212.104.18/accessible_media_program"
print(psql_connection)
engine = create_engine(psql_connection,
                       connect_args={'options': '-csearch_path={}'.format("main"),
                                     'connect_timeout': 5,
                                     'application_name': "application"},
                       client_encoding='utf8',
                       pool_size=50,
                       max_overflow=10,
                       pool_recycle=300,
                       pool_pre_ping=True,
                       pool_use_lifo=True
                       )
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind=engine)


def get_session():

    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()



