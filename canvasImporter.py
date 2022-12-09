
import subprocess
import json, sys

from accessConnection import get_session, CanvasImport

script_locations = {
    "script_location": r"C:\Users\913678186\IdeaProjects\Canvas-Bot\bat\run.bat",
    "output_folder": r"C:\Users\913678186\IdeaProjects\Canvas-Bot\output\json",
    "script_location_home": r"C:\Users\DanielPC\Desktop\Servers\Canvas-Bot\bat\run_home.bat",
    "output_folder_home": r"C:\Users\DanielPC\Desktop\Servers\Canvas-Bot\output\json"

}



def scrape_course(course_id):

    subprocess.run(f'{script_locations["script_location_home"]} {course_id}',
                   shell=True)


def import_raw_data(course_id, semester, course_gen_id):


    session = get_session()


    with open(f"{script_locations['output_folder_home']}\{course_id}.json", 'r') as json_file:
        content = json.loads(json_file.read())
        content_keys = content['content'].keys()

        for content_key in content_keys:

            content_to_load = content['content'][content_key]['content']

            for each in content_to_load:
                print(each)
                test_if_exists = session.query(CanvasImport).filter_by(uri=each['url'],
                                                             course_id=course_id,
                                                             semester=semester).first()


                if not test_if_exists:

                    session.add(CanvasImport(
                        content_type=content_key,
                        resource_type=each['source_page_type'],
                        uri=each['url'],
                        scan_date=each['scan_date'],
                        title=each['title'],
                        course_id=content['course_id'],
                        course_gen_id=course_gen_id,
                        page_component_count=each['order'],
                        source_page_title=each['source_page_title'],
                        mime_type=each['mime_type'],
                        source_page_url=each['source_page_url'],
                        content_hidden=each['is_hidden'],
                        semester=semester,
                        alt_tag_present=each.get('alt_tag_present'),
                        downloadable=each['downloadable'],
                        content_path=each['uri_path'],
                        title_path=each['title_path']

                    ))

    session.commit()
    session.close()


scrape_course("1408")
import_raw_data("1408", "fa22", "fa22CJ50102")