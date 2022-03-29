
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
    print(request)
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




def pdf_accessibility_check(conversion_id: int, stage: str):

    session = get_session()






    conversion = session.query(FileConversions, Files)\
        .join(Files, FileConversions.file_id == Files.id).filter(FileConversions.id==conversion_id).first()

    try:
        check = pdf_check(os.path.join(conversion[0].project_dir, stage, conversion[1].file_name))

        check_meta_assign = session.query(PDFMetadataAssignments).filter_by(conversion_file_id = conversion[0].id).first()

        if check_meta_assign:

            existing_meta_record = session.query(PDFMetadata).filter_by(id=check_meta_assign.metadata_id).first()

            print(conversion[0].id)

            existing_meta_record.is_tagged = check['tagged']
            existing_meta_record.text_type = check['pdf_text_type']
            existing_meta_record.total_figures = len(check['alt_tag_count'])
            existing_meta_record.total_alt_tags = len([True for x in check['alt_tag_count'] if x is True])
            existing_meta_record.stage_folder = "source"
            existing_meta_record.title_set = check['metadata']['title']
            existing_meta_record.lang_set = check['metadata']['language']

            session.commit()

        else:

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
                stage_folder = stage,
                conversion_file_id = conversion[0].id
            )

            session.add(assignment)
            session.commit()

    except PermissionError:
        print("No Access")


def bulk_pdf_check(conversion_id: int, stage: str):

    if stage not in ["source", "active", "complete"]:
        raise Exception("Allowed Stages are: source, active, complete")


    session = get_session()
    conversions = session.query(FileConversions).filter_by(conversion_req_id = conversion_id).all()

    for conversion in conversions:
        pdf_accessibility_check(conversion.id, stage)



bulk_pdf_check(1, "source")