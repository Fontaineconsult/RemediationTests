
import sys, os
import shutil
from accessConnection import get_session, Files, Videos, ConversionRequests, FileConversions
from pdfValidation import pdf_status

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


        if not os.path.isfile(os.path.join(project_files_dir, file.file_hash, 'source', file.file_name)):

            shutil.copyfile(file.file_location,
                            os.path.join(project_files_dir, file.file_hash, 'source', file.file_name))


        source_path = os.path.normpath(file.file_location).split("\\")[3:-1]
        source_hierachy = os.path.join(*source_path)

        if file.file_type == ".pdf":
            pdf_check = pdf_status(file.file_location)
            fileconversion = FileConversions(

                conversion_req_id = request.id,
                source_hierarchy = source_hierachy,
                project_dir = os.path.join(project_files_dir, file.file_hash),
                pdf_access_check = pdf_check

            )
            session.add(fileconversion)




    session.commit()
    session.close()








create_file_conversion(1)