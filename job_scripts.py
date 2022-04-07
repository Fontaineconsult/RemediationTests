
import sys, os
import shutil
from accessConnection import get_session,\
    Files, Videos, ConversionRequests, FileConversions,\
    PDFMetadata, PDFMetadataAssignments, ConversionFilesAssignments,\
    SourceStageViewPDF, CompleteStageViewPDF, ActiveStageViewPDF
from pdfValidation import pdf_status, check_if_tagged, check_for_alt_tags, pdf_check
import hashlib
sys.path.append(r"C:\Users\913678186\IdeaProjects\Moodle_Scraper_V3")
sys.path.append(r"C:\Users\DanielPC\Desktop\Moodle_Scraper_V3")

hasher = hashlib.sha256()

from content_scaffolds.file import ContentFile
from core_classes.iLearnPage import iLearnPage
from network.session_manager import MoodleSession

download_dir = r"Z:\ACRS\Requests"
project_files_dir = r"Z:\ACRS\project_files"


def create_file_conversion(request_id: int):

    """
    Copies files from staging directory and moves them into project directory staged.
    :param request_id:
    :return:
    """

    session = get_session()

    request = session.query(ConversionRequests).filter_by(id=request_id).first()
    print(request)
    files = session.query(Files).filter_by(origin_requester_id = request.conversion_requester).all()

    videos = session.query(Videos).filter_by(origin_requester_id = request.conversion_requester).all()

    for file in files:
        print(file)
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

            new_file = Files(
                file_hash=file.file_hash,
                file_name=file.file_name,
                file_location= os.path.join(project_files_dir, file.file_hash, 'source', file.file_name),
                file_type=file.file_type,
                origin_requester_id = file.origin_requester_id

            )

            session.add(new_file)
            source_path = os.path.normpath(file.file_location).split("\\")[3:-1]
            source_hierachy = os.path.join(*source_path)

            if file.file_type == ".pdf":

                fileconversion=FileConversions(
                    conversion_req_id=request.id,
                    source_hierarchy=source_hierachy,
                    project_dir=os.path.join(project_files_dir, file.file_hash),

                )
                session.add(fileconversion)

                session.flush()

                assignment = ConversionFilesAssignments(

                    conversion_id=fileconversion.id,
                    file_id=new_file.id,
                    stage="source",
                )
                session.add(assignment)

                session.commit()
    session.close()


def start_pdf_file_conversion(file_conversion_id: int):

    """
    Moves files into Active Directory and creates DB entries.
    :param file_conversion_id:
    :return:
    """
    session = get_session()
    request = session.query(SourceStageViewPDF).filter_by(conversion_id=file_conversion_id).first()
    if not os.path.isdir(os.path.join(project_files_dir, request.file_hash, "active")):
        os.mkdir(os.path.join(project_files_dir, request.file_hash, "active"))

    if not os.path.isfile(os.path.join(project_files_dir, request.file_hash, 'active', request.file_name)):

        shutil.copyfile(request.file_location,
                        os.path.join(project_files_dir, request.file_hash, 'active', request.file_name))

    record_exists = session.query(ActiveStageViewPDF).filter_by(file_hash=request.file_hash).first()

    if record_exists:
        return record_exists.file_id

    new_file = Files(
        file_hash=request.file_hash,
        file_name=request.file_name,
        file_location= os.path.join(project_files_dir, request.file_hash, 'active', request.file_name),
        file_type=request.file_type,
        origin_requester_id = request.origin_requester_id

    )

    session.add(new_file)
    session.flush()
    new_file_id = new_file.id
    assignment = ConversionFilesAssignments(

        conversion_id=request.conversion_id,
        file_id=new_file.id,
        stage="active",
    )
    session.add(assignment)

    session.commit()
    session.close()

    return new_file_id


def finalize_pdf_file_conversion(file_conversion_id: int):
    session = get_session()
    request = session.query(ActiveStageViewPDF).filter_by(conversion_id=file_conversion_id).first()

    if not os.path.isdir(os.path.join(project_files_dir, request.file_hash, "complete")):
        os.mkdir(os.path.join(project_files_dir, request.file_hash, "complete"))

    if not os.path.isfile(os.path.join(project_files_dir, request.file_hash, 'complete', request.file_name)):

        shutil.copyfile(request.file_location,
                        os.path.join(project_files_dir, request.file_hash, 'complete', request.file_name))

    record_exists = session.query(CompleteStageViewPDF).filter_by(file_hash=request.file_hash).first()

    if record_exists:
        return record_exists.file_id

    new_file = Files(
        file_hash=request.file_hash,
        file_name=request.file_name,
        file_location= os.path.join(project_files_dir, request.file_hash, 'complete', request.file_name),
        file_type=request.file_type,
        origin_requester_id = request.origin_requester_id

    )

    session.add(new_file)
    session.flush()
    new_file_id = new_file.id
    assignment = ConversionFilesAssignments(

        conversion_id=request.conversion_id,
        file_id=new_file.id,
        stage="complete",
    )
    session.add(assignment)

    session.commit()
    session.close()

    return new_file_id






def pdf_accessibility_check(conversion_id: int, stage: str):

    session = get_session()

    conversion = session.query(FileConversions, ConversionFilesAssignments, Files)\
        .join(ConversionFilesAssignments, FileConversions.id == ConversionFilesAssignments.conversion_id)\
        .join(Files, ConversionFilesAssignments.file_id == Files.id).filter(FileConversions.id==conversion_id)\
        .filter(ConversionFilesAssignments.stage == stage).first()

    # conversion = session.query(FileConversions, Files)\
    #     .join(Files, FileConversions.file_id == Files.id).filter(FileConversions.id==conversion_id).first()

    try:
        check = pdf_check(os.path.join(conversion[0].project_dir, stage, conversion[2].file_name))

        check_meta_assign = session.query(PDFMetadataAssignments).filter_by(file_id = conversion[1].file_id).first()

        if check_meta_assign:

            existing_meta_record = session.query(PDFMetadata).filter_by(id=check_meta_assign.metadata_id).first()
            existing_meta_record.is_tagged = check['tagged']
            existing_meta_record.text_type = check['pdf_text_type']
            existing_meta_record.total_figures = len(check['alt_tag_count'])
            existing_meta_record.total_alt_tags = len([True for x in check['alt_tag_count'] if x is True])
            existing_meta_record.stage_folder = "source"
            existing_meta_record.title_set = check['metadata']['title']
            existing_meta_record.lang_set = check['metadata']['language']
            existing_meta_record.number_of_pages=check['doc_data']['pages']

            session.commit()

        else:

            metadata = PDFMetadata(
                is_tagged=check['tagged'],
                text_type=check['pdf_text_type'],
                total_figures=len(check['alt_tag_count']),
                total_alt_tags=len([True for x in check['alt_tag_count'] if x is True]),
                stage_folder="source",
                title_set=check['metadata']['title'],
                lang_set=check['metadata']['language'],
                number_of_pages=check['doc_data']['pages']

            )

            session.add(metadata)
            session.flush()
            session.refresh(metadata)

            assignment = PDFMetadataAssignments(
                metadata_id = metadata.id,
                file_id = conversion[1].file_id
            )

            session.add(assignment)
            session.commit()

    except PermissionError:
        print("No Access")


def bulk_pdf_check(requester_id: int, stage: str):

    if stage not in ["source", "active", "complete"]:
        raise Exception("Allowed Stages are: source, active, complete")

    session = get_session()

    if stage == "source":
        conversions = session.query(SourceStageViewPDF).filter_by(requester_id=requester_id).all()

    if stage == "active":
        conversions = session.query(ActiveStageViewPDF).filter_by(requester_id=requester_id).all()
        print(conversions)

    if stage == "complete":
        conversions = session.query(CompleteStageViewPDF).filter_by(requester_id=requester_id).all()

    for conversion in conversions:
        pdf_accessibility_check(conversion.conversion_id, stage)



def send_to_abby_server(conversion_id:int):

    session = get_session()
    request = session.query(ActiveStageViewPDF).filter_by(conversion_id=conversion_id).first()
    print(request)



send_to_abby_server(852)

# create_file_conversion(5)
# bulk_pdf_check(5, "source")
# pdf_accessibility_check(844, "active")