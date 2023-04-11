import glob, sys, os
import hashlib
# from accessConnection import get_session, Files, Videos

sys.path.append(r"C:\Users\913678186\IdeaProjects\Moodle_Scraper_V3")
sys.path.append(r"C:\Users\DanielPC\Desktop\Moodle_Scraper_V3")
from content_scaffolds.file import ContentFile
from core_classes.iLearnPage import iLearnPage
from network.session_manager import MoodleSession
download_dir = r"Z:\ACRS\Requests"


# session = get_session()

def clean_filename(name: str):
    name = name.replace("%", "")
    name = name.replace("=", "")
    name = name.replace("?", "")
    name = name.replace("*", "")
    name = name.replace(":", "")
    name = name.replace("'", "")
    name = name.replace(",", "")
    name = name.replace('"', "")
    name = name.replace('|', "")
    name = name.replace('/', "")
    name = name.rstrip()
    name = name.lstrip()
    return name

    # ("OL-StrategiesSuccess", "collab", "2152", 3),
    # ("PHIL 101.01", "standard", "18241", 1),
    # ("E_ED 0786-07", "standard", "14719", 2),
    # ("AAS 510 Temp Shell", "collab", "2191", 5)

pages = [



        ("ENG 0583-01", "standard", "8658", 6)
]


def download(node: ContentFile, course_folder: str, section_folder: str, page_session: MoodleSession):
    if not os.path.exists(os.path.join(download_dir, course_folder, section_folder)):
        os.makedirs(os.path.join(download_dir, course_folder, section_folder))  # create folder if it does not exist
    if node.file_name is not None:
        filename = node.file_name
    else:
        filename = node.url.split('/')[-1].replace(" ", "_")  # be careful with file names

    filename = clean_filename(filename)

    r = page_session.get(node.url)
    print("NODE URL", node.url)
    if r.ok:
        file_path = os.path.join(download_dir, course_folder, section_folder, filename)
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        return file_path
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        return None




for page in pages:
    print("Starting -----  ", page[0])
    ilearnpage = iLearnPage(page[1], page[2],"3948ead63a9f2944218de038d8934305")
    ilearnpage.init_session()
    ilearnpage.scrape()
    page_content = ilearnpage.get_content()
    for content in page_content:
        section = page_content[content]
        for item in section:
            if item.downloadable:

                file_location = download(item, page[0], clean_filename(content.section_title), ilearnpage.session)

                if file_location:
                    if os.path.isfile(file_location):
                        with open(file_location, 'rb') as afile:
                            buf = afile.read()
                            hasher = hashlib.sha256()
                            hasher.update(buf)
                            file_hash = hasher.hexdigest()
                    # file_exists = session.query(Files).filter_by(file_location=file_location).first()

                    # if not file_exists:
                    #     file = Files(
                    #         file_hash = hasher.hexdigest(),
                    #         file_name = os.path.basename(file_location),
                    #         file_location = file_location,
                    #         file_type = os.path.splitext(file_location)[1],
                    #         origin_requester_id=page[3]
                    #     )
                    #     session.add(file)
                    #     session.commit()
                    #     session.close()

            # if item.is_video:
            #     video_exists = session.query(Videos).filter_by(source_url=item.url).first()
            #     if not video_exists:
            #         file = Videos(
            #             media_type = "Not Sure",
            #             title = item.title,
            #             source_url = item.url,
            #             origin_requester_id=page[3]
            #         )
            #         session.add(file)
            #         session.commit()
            #         session.close()











