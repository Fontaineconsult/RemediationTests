
import sys, os
import shutil
from accessConnection import get_session,\
    Files, Videos, ConversionRequests, FileConversions, PDFMetadata, PDFMetadataAssignments
from pdfValidation import pdf_status, check_if_tagged, check_for_alt_tags, pdf_check

sys.path.append(r"C:\Users\913678186\IdeaProjects\Moodle_Scraper_V3")
sys.path.append(r"C:\Users\DanielPC\Desktop\Moodle_Scraper_V3")

from content_scaffolds.file import ContentFile
from core_classes.iLearnPage import iLearnPage
from network.session_manager import MoodleSession

download_dir = r"Z:\ACRS\Requests"
project_files_dir = r"Z:\ACRS\project_files"


def create_file_conversion(request_id):
    session = get_session()

    request = session.query(ConversionRequests).filter_by(id=request_id).first()
    files = session.query(Files).filter_by(origin_requester_id = request.conversion_requester).all()
    videos = session.query(Videos).filter_by(origin_requester_id = request.conversion_requester).all()

    for file in files:
        if not os.path.isdir(os.path.join(project_files_dir, file.file_hash)):
            os.mkdir(os.path.join(project_files_dir, file.file_hash))
            if not os.path.isdir(os.path.join(project_files_dir, file.file_hash, "source")):
                os.mkdir(os.path.join(project_files_dir, file.file_hash, "source"))
            if not os.path.isdir(os.path.join(project_files_dir, file.file_hash, "active")):
                os.mkdir(os.path.join(project_files_dir, file.file_hash, "active"))
            if not os.path.isdir(os.path.join(project_files_dir, file.file_hash, "complete")):
                os.mkdir(os.path.join(project_files_dir, file.file_hash, "complete"))

        if not os.path.isfile(os.path.join(project_files_dir, file.file_hash, 'source', file.file_name)):

            shutil.copyfile(file.file_location,
                            os.path.join(project_files_dir, file.file_hash, 'source', file.file_name))

        source_path = os.path.normpath(file.file_location).split("\\")[3:-1]
        source_hierachy = os.path.join(*source_path)

        if file.file_type == ".pdf":

            fileconversion = FileConversions(
                file_id = file.id,
                conversion_req_id = request.id,
                source_hierarchy = source_hierachy,
                project_dir = os.path.join(project_files_dir, file.file_hash),


            )
            session.add(fileconversion)

    session.commit()
    session.close()


# create_file_conversion(1)

def pdf_accessibility_check(conversion_id: int, stage: str):

    session = get_session()
    conversion = session.query(FileConversions, Files)\
        .join(Files, FileConversions.file_id == Files.id).filter(FileConversions.id==conversion_id).first()


    print(conversion)
    try:
        check = pdf_check(os.path.join(conversion[0].project_dir, stage, conversion[1].file_name))

        metadata = PDFMetadata(
            is_tagged=check['tagged'],
            text_type=check['pdf_text_type'],
            total_figures=len(check['alt_tag_count']),
            total_alt_tags=len([True for x in check['alt_tag_count'] if x is True]),
            stage_folder="source",
            title_set=check['metadata']['title'],
            lang_set=check['metadata']['language']

        )

        session.add(metadata)
        session.flush()
        session.refresh(metadata)

        assignment = PDFMetadataAssignments(
            metadata_id = metadata.id,
            conversion_file_id = conversion[0].id
        )

        session.add(assignment)
        session.commit()

    except PermissionError:
        print("No Access")



pdf_accessibility_check(876, "source")
