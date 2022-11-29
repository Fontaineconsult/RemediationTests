





for course_id in course_ids:
    scrape = subprocess.run(f'{canvas_bot["script_location"]} {course_id.canvas_page_id}',
                            shell=True)
