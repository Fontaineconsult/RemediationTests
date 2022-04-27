
import sys, os
import shutil
from accessConnection import get_session,\
    Files, Videos, ConversionRequests, FileConversions,\
    PDFMetadata, PDFMetadataAssignments, ConversionFilesAssignments,\
    SourceStageViewPDF, CompleteStageViewPDF, ActiveStageViewPDF, AbbyyServerJobs
from pdfValidation import pdf_check
from WebAPI import create_abbyy_job, check_abbyy_job_status, get_abbyy_job_result, save_job_file

import hashlib
sys.path.append(r"C:\Users\913678186\IdeaProjects\Moodle_Scraper_V3")
sys.path.append(r"C:\Users\DanielPC\Desktop\Moodle_Scraper_V3")

hasher = hashlib.sha256()



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
                    finalized=False

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

            if file.file_type == '.docx' or file.file_type == '.doc':

                fileconversion=FileConversions(
                    conversion_req_id=request.id,
                    source_hierarchy=source_hierachy,
                    project_dir=os.path.join(project_files_dir, file.file_hash),
                    finalized=False

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

    if request:

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

    else:
        print("No Item Found")

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
        print("EXISTS")
        finalize = session.query(FileConversions).filter_by(id=file_conversion_id).first()
        print(finalize)
        existing_file_id = record_exists.file_id
        if finalize:
            print("FINALIZED", finalize.project_dir, finalize.finalized)
            finalize.finalized = True
            session.commit()
            session.close()
        return existing_file_id

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

    finalize = session.query(FileConversions).filter_by(id=file_conversion_id).first()

    if finalize:
        finalize.finalized = True

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
        check = pdf_check(os.path.join(conversion[2].file_location))
        if check:
            print(check)
            check_meta_assign = session.query(PDFMetadataAssignments).filter_by(file_id = conversion[1].file_id).first()

            if check_meta_assign:
                print("CHECK")
                update_abbyy_job_status(conversion[1].file_id)
                existing_meta_record = session.query(PDFMetadata).filter_by(id=check_meta_assign.metadata_id).first()
                existing_meta_record.is_tagged = check['tagged']
                existing_meta_record.text_type = check['pdf_text_type']
                existing_meta_record.total_figures = len(check['alt_tag_count'])
                existing_meta_record.total_alt_tags = len([True for x in check['alt_tag_count'] if x is True])
                existing_meta_record.stage_folder = "source"
                existing_meta_record.title_set = check['metadata']['title']
                existing_meta_record.lang_set = check['metadata']['language']
                existing_meta_record.number_of_pages= check['doc_data']['pages']
                existing_meta_record.headings_pass = check['headings_pass']

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
                    number_of_pages=check['doc_data']['pages'],
                    headings_pass=check['headings_pass']

                )

                session.add(metadata)
                session.flush()
                session.refresh(metadata)

                assignment = PDFMetadataAssignments(
                    metadata_id = metadata.id,
                    file_id = conversion[1].file_id
                )
                print("CHECK")
                update_abbyy_job_status(conversion[1].file_id)
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

    file_exists = session.query(AbbyyServerJobs).filter_by(file_id=request.file_id).first()

    if file_exists:

        job_id = create_abbyy_job(request.file_location)
        file_exists.abbyy_job_id = job_id
        file_exists.state = "first_init"
        update_abbyy_job_status(request.file_id)
        session.commit()

        return job_id

    else:

        job_id = create_abbyy_job(request.file_location)
        abbyJob = AbbyyServerJobs(
            abbyy_job_id = job_id,
            file_id = request.file_id,
            state = "first_init"

        )
        session.add(abbyJob)
        server_job_id = abbyJob.id
        file_id = request.file_id
        session.commit()
        update_abbyy_job_status(file_id)
        session.close()
        return server_job_id



def update_abbyy_job_status(file_id):
    session = get_session()
    abbyyJob = session.query(AbbyyServerJobs).filter_by(file_id=file_id).first()
    if abbyyJob:
        print("check_status")
        status = check_abbyy_job_status(abbyyJob.abbyy_job_id)
        print(status)
        abbyyJob.state = status['State']
        abbyyJob.progress = status['Progress']
        session.commit()
        session.close()
    else:
        print("NO ID FOUND")


def replace_old_file_with_abbyy_file(abbyy_job_id, file_location):
    abbyy_file = get_abbyy_job_result(abbyy_job_id)
    session = get_session()
    record = session.query(ActiveStageViewPDF).filter_by(file_location=file_location).first()
    file_location = os.path.split(file_location)[0]
    save_job_file(abbyy_file, file_location)
    print(file_location)
    file = session.query(Files).filter_by(id=record.file_id).first()
    file.file_location = os.path.join(file_location, abbyy_file.FileName)
    session.commit()
    session.close()


def deactivate_active_job(conversion_id):
    session = get_session()
    conversion_assignment = session.query(ConversionFilesAssignments)\
        .filter(ConversionFilesAssignments.conversion_id == conversion_id,
                ConversionFilesAssignments.stage == "active").first()
    print(conversion_assignment)



    if conversion_assignment:
        file = session.query(Files).filter_by(file_id=conversion_assignment.file_id).first()
        if file:

            os.remove(file.file_location)
            session.delete(conversion_assignment)
            session.commit()




# deactivate_active_job(988)





# replace_old_file_with_abbyy_file("{CFD57D54-2641-4AF3-B2DD-D9108F187D22}", r"Z:\ACRS\project_files\21d84e435c4ceee24482f4db21dfd89e10268fe6fb5fa0815a93a3dae6096d8c\active\2007_Claudia Lang.pdf")


# send_to_abby_server(852)
# update_abbyy_job_status(1245)

# create_file_conversion(5)
# bulk_pdf_check(5, "source")
# pdf_accessibility_check(844, "active")