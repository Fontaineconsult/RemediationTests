import glob, sys, os
import hashlib
from accessConnection import get_session, Files

test = Files
sys.path.append(r"C:\Users\913678186\IdeaProjects\Moodle_Scraper_V3")

from src.interface.downloader import get_all_ilearn_page_files

download_dir = r"Z:\ACRS\Requests"

pages = [
        ("OL-StrategiesSuccess", "collab", "2152"),
         ("PHIL 101.01", "standard", "18241"),
         ("E_ED 0786-07", "standard", "14719")
]

get_all_ilearn_page_files(pages,download_dir)

hasher = hashlib.sha256()

downloaded_files = glob.glob(r"Z:\ACRS\Requests" + '\**\*[.pdf|.docx|.doc]', recursive=True)

session = get_session()


print(downloaded_files)

for each in downloaded_files:

    if os.path.isfile(each):
        with open(each, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
            hasher.hexdigest()


    file_exists = session.query(Files).filter_by(file_location = each).first()

    if not file_exists:
        file = Files(
            file_hash = hasher.hexdigest(),
            file_name = os.path.basename(each),
            file_location = each,
            file_type = os.path.splitext(each)[1]
        )
        session.add(file)
        session.commit()
        session.close()

