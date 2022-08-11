import re
from typing import Type

import pikepdf
from pikepdf import Object


def look_up_char(octal_code, character_map):
    return_string = ''
    codes = re.findall(re.compile("\(.*?\)"), octal_code)
    for each in codes:
        remove_bracks = each.replace("(", "").replace(")", "")

        split_by_bracks = remove_bracks.split("\\")

        for code in split_by_bracks:

            try:

                # return_string += differences[int(code)]
                return_string += character_map[(int(code, 8))]
            except ValueError:
                continue


def create_character_map(raw_map):

    remove_brackets = raw_map.replace("<", "").replace(">", "")
    remove_new_lines = remove_brackets.split("\n")

    unicode_dict = {}
    for each in remove_new_lines:
        uke = each.split(" ")
        try:
            unicode_dict[int(uke[0], 16)] = chr(int(uke[1], 16))
        except IndexError:
            continue
        except ValueError:
            continue

    for each in unicode_dict:
        print(each, unicode_dict[each])
    return unicode_dict


def get_unicode_maps(page: Object) -> dict:
    capture_re = re.compile("(beginbfchar(.*)endbfchar)", flags=re.DOTALL)
    unicode_maps = dict()
    fonts = page.get("/Resources").get("/Font")

    for font in fonts:
        try:
            raw_map = fonts[font].get("/ToUnicode").read_bytes().decode('utf-8')
            clean_map = re.search(capture_re, raw_map)
            char_map = create_character_map(clean_map.groups()[1])
            unicode_maps[font.strip("/")] = char_map

        except AttributeError:
            print("No Unicode Object Found")
            continue


    return unicode_maps



pdf = pikepdf.open(r"Z:\ACRS\project_files\b39757337fe0b2a33bdb78aaaa13b9afa61e672ae8c13edfbed5f37ecb3a5185\source\Practice Variability.pdf")
page = pdf.pages[5].get("/Contents").read_bytes()
print(repr(page))

print(get_unicode_maps(pdf.pages[5]))