
from sqlalchemy import create_engine, Integer, Column, String, DateTime, Boolean, ForeignKey, ARRAY, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
Base = declarative_base()
from datetime import datetime


class CanvasImport(Base):

    __tablename__ = 'canvas_import'
    id = Column(Integer, primary_key=True)
    resource_type = Column(String)
    content_type = Column(String)
    downloadable = Column(Boolean, default=True)
    is_hidden = Column(Boolean, default=False)
    mime_type = Column(String)
    order = Column(Integer)
    scan_date = Column(DateTime)
    source_page_title = Column(String)
    source_page_url = Column(String)
    title = Column(String)
    uri = Column(String)
    course_id = Column(String)
    alt_tag_present = Column(Boolean, default=False)
    semester = Column(String)
    course_gen_id = Column(String)
    page_component_count = Column(Integer)
    parent_url = Column(String)
    content_hidden = Column(String)
    content_path = Column(ARRAY(String))
    title_path = Column(ARRAY(String))
    scan_object = Column(LargeBinary())


### User Data ###

class Courses(Base):

    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(50))
    course_gen_id = Column(String(20))
    ilearn_id = Column(String(50))
    semester = Column(String(50))
    canvas_id = Column(String(20))


class EmployeeCourseAssignments(Base):

    __tablename__ = 'employee_course_assignments'
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(9),  ForeignKey("employee.employee_id"))
    course_id = Column(Integer(), ForeignKey("courses.id"))

class StudentCourseAssignments(Base):

    __tablename__ = 'student_course_assignments'
    id = Column(Integer, primary_key=True)
    student_id = Column(String(9),  ForeignKey("students.student_id"))
    course_id = Column(Integer(), ForeignKey("courses.id"))


class CampusAssociation(Base):

    __tablename__ = 'campus_association'
    id = Column(Integer, primary_key=True)
    campus_org_id = Column(Integer, ForeignKey("orgs.id"))
    employee_id = Column(String(9), ForeignKey("employee.employee_id"))


class Students(Base):

    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    email = Column(String())


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
    course_assignment_id = Column(Integer(), ForeignKey("courses.id"))
    campus_association_id = Column(Integer(), ForeignKey("campus_association.id"))

### Canvas Reviews ###

class CanvasAccessibilityReviews(Base):

    __tablename__ = 'canvas_accessibility_review'
    id = Column(Integer, primary_key=True)
    conversion_requester = Column(Integer(), ForeignKey("conversion_requester.id"))
    json_output_path = Column(String())


class AccessibilityReviewNotes(Base):

    __tablename__ = 'canvas_accessibility_review_notes'
    id = Column(Integer, primary_key=True)
    canvas_review_id = Column(Integer(), ForeignKey("canvas_accessibility_review.id"))

class CanvasAccessibilityReviewContentAssignments(Base):

    __tablename__ = 'canvas_accessibility_review_assignment'
    id = Column(Integer, primary_key=True)
    canvas_review_id = Column(Integer(), ForeignKey("canvas_accessibility_review.id"))
    accessibility_meta_data_assignment = Column(Integer(), ForeignKey("accessibility_metadata_assignment.id"))


class CanvasReviewMeta(Base):

    __tablename__ = 'canvas_accessibility_review_meta'
    id = Column(Integer, primary_key=True)
    canvas_review = Column(Integer(), ForeignKey("canvas_accessibility_review.id"))
    comments = Column(String())


### Accessibility Metadata ###

class AccessibilityMetaDataAssignment(Base):

    __tablename__ = 'accessibility_metadata_assignment'

    id = Column(Integer, primary_key=True)
    document_file_id = Column(Integer(), ForeignKey("documents.id"))
    pdf_accessibility_meta = Column(Integer(), ForeignKey("pdf_accessibility_metadata.id"))
    msword_accessibility_meta = Column(Integer(), ForeignKey("msword_accessibility_metadata.id"))
    image_file_id = Column(Integer(), ForeignKey("images.id"))
    image_meta_id = Column(Integer(), ForeignKey("images_accessibility_metadata.id"))
    video_links_id = Column(Integer(), ForeignKey("video_links.id"))
    video_links_meta_id = Column(Integer(), ForeignKey("video_links_accessibility_metadata.id"))
    video_files_id = Column(Integer(), ForeignKey("video_files.id"))
    video_files_meta_id = Column(Integer(), ForeignKey("video_files_accessibility_metadata.id"))
    audio_links_id = Column(Integer(), ForeignKey("audio_links.id"))
    audio_links_meta_id = Column(Integer(), ForeignKey("audio_links_accessibility_metadata.id"))
    audio_files_id = Column(Integer(), ForeignKey("audio_files.id"))
    audio_files_meta_id = Column(Integer(), ForeignKey("audio_files_accessibility_metadata.id"))
    pseudo_content_id = Column(Integer(), ForeignKey("pseudo_content.id"))
    pseudo_content_meta_id = Column(Integer(), ForeignKey("pseudo_content_accessibility_metadata.id"))


class ImagesAccessibilityMeta(Base):

    __tablename__ = 'images_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class PDFAccessibilityMeta(Base):

    __tablename__ = 'pdf_accessibility_metadata'
    id = Column(Integer, primary_key=True)
    is_tagged = Column(Boolean(), default=False)
    text_type = Column(Integer())
    total_figures = Column(Integer())
    total_alt_tags = Column(Integer())
    has_doc_desc = Column(Boolean(), default=False)
    stage_folder = Column(String())
    title_set = Column(Boolean(), default=False)
    lang_set = Column(Boolean(), default=False)
    number_of_pages = Column(Integer())
    headings_pass = Column(Boolean(), default=False)
    has_bookmarks = Column(Boolean(), default=False)


class MSWordAccessibilityMeta(Base):

    __tablename__ = 'msword_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class VideoLinksAccessibilityMeta(Base):

    __tablename__ = 'video_links_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class VideoFilesAccessibilityMeta(Base):

    __tablename__ = 'video_files_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class AudioLinksAccessibilityMeta(Base):

    __tablename__ = 'audio_links_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class AudioFilesAccessibilityMeta(Base):

    __tablename__ = 'audio_files_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class PseudoContentAccessibilityMeta(Base):

    __tablename__ = 'pseudo_content_accessibility_metadata'
    id = Column(Integer, primary_key=True)

### Content Tacking ###


class Images(Base):

    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)


class Documents(Base):

    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)


class VideoLinks(Base):

    __tablename__ = 'video_links'
    id = Column(Integer, primary_key=True)
    uri = Column(String())


class VideoFiles(Base):

    __tablename__ = 'video_files'
    id = Column(Integer, primary_key=True)


class AudioLinks(Base):

    __tablename__ = 'audio_links'
    id = Column(Integer, primary_key=True)
    uri = Column(String())


class AudioFiles(Base):

    __tablename__ = 'audio_files'
    id = Column(Integer, primary_key=True)


class PseudoContent(Base):

    __tablename__ = 'pseudo_content'
    id = Column(Integer, primary_key=True)
    uri = Column(String())


### File Tracking ###


class FileAssignments(Base):
    __tablename__ = 'file_assignments'
    id = Column(Integer, primary_key=True)
    document_files_id = Column(Integer(), ForeignKey("documents.id"))
    video_files_id = Column(Integer(), ForeignKey("video_files.id"))
    audio_files_id = Column(Integer(), ForeignKey("audio_files.id"))
    file_id = Column(Integer(), ForeignKey("files.id"))


class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_hash = Column(String())
    file_name = Column(String())
    file_location = Column(String())
    file_type = Column(String())



### Conversion Tracking ###


class GeneralConversionAssignement(Base):

    __tablename__ = 'general_conversion_assignments'
    id = Column(Integer, primary_key=True)
    conversion_task_id = Column(Integer(), ForeignKey("conversions_tasks.id"))
    conversion_requester_id = Column(Integer(), ForeignKey("conversion_requester.id"))


class CanvasReviewConversionAssignment(Base):

    __tablename__ = 'canvas_conversion_assignments'
    id = Column(Integer, primary_key=True)
    conversion_task_id = Column(Integer(), ForeignKey("conversions_tasks.id"))
    canvas_content_assignment = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))


class ConversionTasks(Base):

    __tablename__ = 'conversions_tasks'
    id = Column(Integer, primary_key=True)
    stage = Column(String())
    comments = Column(String())


class ConversionTypeAssignment(Base):

    __tablename__ = 'conversion_type_assignment'
    id = Column(Integer, primary_key=True)
    pdf_conversion_job_id = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))
    ms_word_conversion_job_id = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))
    ocr_job_id = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))
    audio_conversion_job_id = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))
    power_point_conversion_job_id = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))
    captioning_job_id = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))
    transcript_job_id = Column(Integer(), ForeignKey("canvas_accessibility_review_assignment.id"))




### Accessible Conversion Jobs ###


class PDFJobs(Base):

    __tablename__ = 'pdf_jobs'
    id = Column(Integer, primary_key=True)


class MSWordJobs(Base):

    __tablename__ = 'ms_word_jobs'
    id = Column(Integer, primary_key=True)


class OCR_jobs(Base):

    __tablename__ = 'ocr_jobs'
    id = Column(Integer, primary_key=True)


class captioning_jobs(Base):

    __tablename__ = 'captioning_jobs'
    id = Column(Integer, primary_key=True)

class AudioJobs(Base):

    __tablename__ = 'audio_jobs'
    id = Column(Integer, primary_key=True)



## Old ##


# class BoxLocations(Base):
#
#     __tablename__ = "box_locations"
#     id = Column(Integer, primary_key=True)
#     box_url = Column(String())
#     owner = Column(String(), ForeignKey("employee.employee_id"))
#     is_active = Column(Boolean())
#
#
# class BoxAssociations(Base):
#
#     __tablename__ = 'box_associations'
#     id = Column(Integer, primary_key=True)
#     box_id = Column(String(50))
#     conversion_id = Column(String())
#
# class AbbyyServerJobs(Base):
#
#     __tablename__ = 'abbyyserverjobs'
#     id = Column(Integer, primary_key=True)
#     abbyy_job_id = Column(String(50))
#     file_id = Column(Integer, ForeignKey("files.id"))
#     state = Column(String(50))
#     progress = Column(Integer())
#
#
#
# class FileConversions(Base):
#
#     __tablename__ = 'file_conversions'
#     id = Column(Integer, primary_key=True)
#     source_hierarchy = Column(String())
#     conversion_req_id = Column(Integer(), ForeignKey("conversion_requests.id"))
#     project_dir = Column(String())
#     file_type = Column(String())
#     finalized = Column(Boolean(), default=False)
#     comments = Column(String())
#
#
#
#
#
#
#
#
#
# class SourceStageViewPDF(Base):
#
#     __tablename__ = 'source_stage_pdf'
#     is_tagged = Column(Boolean())
#     text_type = Column(Integer())
#     total_figures = Column(Integer())
#     total_alt_tags = Column(Integer())
#     title_set = Column(Boolean())
#     lang_set = Column(Boolean())
#     number_of_pages = Column(Integer())
#     stage = Column(String())
#     source_hierarchy = Column(String())
#     conversion_id = Column(Integer(), primary_key=True)
#     file_name = Column(String())
#     file_location = Column(String())
#     file_hash = Column(String())
#     file_id = Column(Integer())
#     file_type = Column(String())
#     origin_requester_id = Column(Integer())
#     requester_id = Column(Integer())
#
#
#
# class ActiveStageViewPDF(Base):
#
#     __tablename__ = 'active_stage_pdf'
#     is_tagged = Column(Boolean())
#     text_type = Column(Integer())
#     total_figures = Column(Integer())
#     total_alt_tags = Column(Integer())
#     title_set = Column(Boolean())
#     lang_set = Column(Boolean())
#     number_of_pages = Column(Integer())
#     stage = Column(String())
#     source_hierarchy = Column(String())
#     conversion_id = Column(Integer(), primary_key=True)
#     file_name = Column(String())
#     file_location = Column(String())
#     file_hash = Column(String())
#     file_id = Column(Integer())
#     file_type = Column(String())
#     origin_requester_id = Column(Integer())
#     requester_id = Column(Integer())
#
#
# class CompleteStageViewPDF(Base):
#
#     __tablename__ = 'complete_stage_pdf'
#     is_tagged = Column(Boolean())
#     text_type = Column(Integer())
#     total_figures = Column(Integer())
#     total_alt_tags = Column(Integer())
#     title_set = Column(Boolean())
#     lang_set = Column(Boolean())
#     number_of_pages = Column(Integer())
#     stage = Column(String())
#     source_hierarchy = Column(String())
#     conversion_id = Column(Integer(), primary_key=True)
#     file_name = Column(String())
#     file_location = Column(String())
#     file_hash = Column(String())
#     file_id = Column(Integer())
#     file_type = Column(String())
#     origin_requester_id = Column(Integer())
#     requester_id = Column(Integer())


#
# print(os.path.isfile(r"C:\\Users\\913678186\\IdeaProjects\\RemediationTests\\ACRS.accdb"))
#
# connection_string = (
#     r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
#     r"DBQ=C:\Users\913678186\IdeaProjects\RemediationTests\ACRS.accdb;"
#     r"ExtendedAnsiSQL=1;")
# connection_uri = f"access+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
# engine = create_engine(connection_uri)


psql_connection = "postgresql://postgres:accesslearning!1@130.212.104.18/amcrp_test"
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



