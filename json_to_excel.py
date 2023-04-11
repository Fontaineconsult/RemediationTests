import json
import openpyxl


def create_excel_file(file_path):
    wb = openpyxl.Workbook()
    wb.create_sheet('Documents')
    wb.create_sheet('Document Sites')
    wb.create_sheet('Image Files')
    wb.create_sheet('Video Files')
    wb.create_sheet('Video Sites')
    wb.create_sheet('Audio')
    wb.create_sheet('Unsorted')
    wb.save(file_path)




def find_key_names(d, path=None):
    if path is None:
        path = []
    result = []
    for k, v in d.items():
        new_path = path + [k]
        if isinstance(v, list):
            result.append(new_path)
        elif isinstance(v, dict):
            sub_result = find_key_names(v, new_path)
            result += sub_result
    return result


def get_column_number(sheet, header_name):
    for col_idx in range(1, sheet.max_column + 1):
        cell = sheet.cell(row=1, column=col_idx)
        if cell.value == header_name:
            return col_idx
    return None


def append_row_by_header(file_path, sheet_name, row_dict):
    wb = openpyxl.load_workbook(file_path)
    try:
        sheet = wb[sheet_name]
    except KeyError:
        sheet = wb.create_sheet(sheet_name)
    header_row = list(sheet[1])
    new_row = []`
    print(row_dict.keys())
    for header_name in row_dict.keys():
        col_num = get_column_number(sheet, header_name)
        print(col_num)
        if col_num is not None:
            new_row.append(row_dict[header_name])
        else:
            print(header_row)
            new_col_letter = openpyxl.utils.get_column_letter(header_row[-1].column_index + 1)
            sheet.cell(row=1, column=header_row[-1].column_index + 1, value=header_name)
            header_row.append(sheet.cell(row=1, column=header_row[-1].column_index + 1))
            new_row.append(row_dict[header_name])
    sheet.append(new_row)
    wb.save(file_path)


def add_sheet_to_excel(file_path, sheet_name, rows, headers):

    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]
    for count, header in enumerate(headers):
        sheet.cell(row=1, column=count).value = header
    for row in rows:
        sheet.append(row)
    wb.save(file_path)


test = r"Z:\ACRS\Cpage\294.json"

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        key_paths = find_key_names(data)
        for path in key_paths:
            # navigate to the list using each path
            sub_dict = data
            for key in path[:-1]:
                sub_dict = sub_dict[key]
            my_list = sub_dict[path[-1]]

            for item in my_list:

                sheet_name = " ".join(word.capitalize() for word in path[-1].replace('_', ' ').split(' '))
                append_row_by_header(r"Z:\ACRS\Cpage\test.xlsx", sheet_name, item)

        # for item in data['content']['documents']['documents']:
        #     print(item)
        #     append_row_by_header(r"Z:\ACRS\Cpage\test.xlsx", 'Documents', item)

        #
        # append_row_by_header(r"Z:\ACRS\Cpage\test.xlsx", 'Documents', data['content']['documents']['document_sites'])

        # print(data['content']['documents']['document_sites'])
        # add_sheet_to_excel(r"Z:\ACRS\Cpagetest.xlsx", 'Documents', data['content']['documents']['documents'], list(data['content']['documents']['documents'][0].keys()))
        # print(data['content']['documents']['documents'])
        # add_sheet_to_excel(r"Z:\ACRS\Cpagetest.xlsx", 'Images', data['content']['images']['image_files'], list(data['content']['images']['image_files'][0].keys()))
        # print(data['content']['unsorted']['unsorted'])
        # add_sheet_to_excel(r"Z:\ACRS\Cpagetest.xlsx", 'Unsorted', data['content']['unsorted']['unsorted'], list(data['content']['unsorted']['unsorted'][0].keys()))
        # print(data['content']['videos']['video_files'])
        # add_sheet_to_excel(r"Z:\ACRS\Cpagetest.xlsx", 'Videos', data['content']['videos']['video_files'], list(data['content']['videos']['video_files'][0].keys()))
        # print(data['content']['videos']['video_sites'])
        # add_sheet_to_excel(r"Z:\ACRS\Cpagetest.xlsx", 'Videos', data['content']['videos']['video_sites'], list(data['content']['videos']['video_sites'][0].keys()))
        # print(data['content']['audio']['audio_files'])
        # add_sheet_to_excel(r"Z:\ACRS\Cpagetest.xlsx", 'Audio', data['content']['audio']['audio_files'], list(data['content']['audio']['audio_files'][0].keys()))
        # print(data['content']['audio']['audio_sites'])
        # print(data['content']['images']['image_files'])


create_excel_file(r"Z:\ACRS\Cpage\test.xlsx")
read_json_file(test)

