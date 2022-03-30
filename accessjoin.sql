SELECT main_file_conversions.id, main_file_conversions.project_dir, main_files.file_name, main_files.file_type, main_pdf_metadata_assignment.stage_folder, main_pdf_metadata.is_tagged, main_pdf_metadata.text_type, main_pdf_metadata.total_figures, main_pdf_metadata.total_alt_tags, main_pdf_metadata.lang_set, main_pdf_metadata.title_set, main_pdf_metadata.number_of_pages, main_conversion_requester.course_id, main_conversion_requester.campus_association_id, main_orgs.org_name, main_courses.course_name
FROM ((((((main_pdf_metadata_assignment INNER JOIN (main_file_conversions INNER JOIN main_files ON main_file_conversions.file_id = main_files.id) ON main_pdf_metadata_assignment.conversion_file_id = main_file_conversions.id) INNER JOIN main_pdf_metadata ON main_pdf_metadata_assignment.metadata_id = main_pdf_metadata.id) INNER JOIN main_conversion_requests ON main_file_conversions.conversion_req_id = main_conversion_requests.id) LEFT JOIN main_conversion_requester ON main_conversion_requests.conversion_requester = main_conversion_requester.id) LEFT JOIN main_courses ON main_conversion_requester.course_id = main_courses.id) LEFT JOIN main_campus_association ON main_conversion_requester.campus_association_id = main_campus_association.id) LEFT JOIN main_orgs ON main_campus_association.campus_org_id = main_orgs.id;