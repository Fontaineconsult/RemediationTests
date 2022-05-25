import pikepdf
from pdfminer import high_level
from pdfminer.layout import LTImage
import pdfminer
from pikepdf import Pdf, Dictionary, Array, String, Object, Name, PdfError, OutlineItem
import re
import hashlib

def _get_page_number_of_page(page_obj: Object, document: Pdf):

    count = 0

    for each in list(document.Root.Pages.Kids):

        if each.get("/Type") == "/Pages":
            for page in each.get("/Kids"):
                count += 1
                if page == page_obj:
                    return count

        else:
            count += 1
            if each == page_obj:
                return count



def page_contains_text(page):
    if page.groups is None:
        return False
    for each in page.groups:
        if isinstance(each, pdfminer.layout.LTTextGroupLRTB):
            return True
    return False


def image_over_text(page):

    for item in list(page):

        if isinstance(item, pdfminer.layout.LTFigure):
            check = False
            for pdf_object in item._objs:
                if isinstance(pdf_object, LTImage):
                    check = True
                if check:
                    variance = ((item.x1 - item.x0) * (item.y1 - item.y0)) / ((page.x1 - page.x0) * (page.y1 - page.y0))
                    if 0.9 < variance < 1.1:  # Check to see if the size of the text image is the same as the page
                        return True
                    else:
                        continue
        continue
    return False


def check_status(document_location):
    pages = list(high_level.extract_pages(document_location))

    to_return = []
    for page in pages:

        image = image_over_text(page)
        text = page_contains_text(page)
        to_return.append((image,text))

    return to_return


def pdf_status(document_location):

    # True True = Image of text over text
    # False True = Text Only
    # True False = Only Image of Text
    # False False = No image of text and no page text

    t1 = 0
    t2 = 0
    page_stats = check_status(document_location)

    for each in page_stats:
        if each[0]:
            t1 += 1
        if each[1]:
            t2 += 1
    print(t1, t2)
    if t1 > 0 and t2 > 0:
        return 0  # Image of text over text
    if t1 == 0 and t2 != 0:
        return 1  # Text Only
    if t1 > 0 and t2 == 0:
        return 2  # Only Image of Text
    if t1 == 0 and t2 == 0:
        return 3  # No image of text and no page text


def check_if_tagged(document):
    if isinstance(document, str):
        pdf = Pdf.open(document)
        if pdf.Root.get("/StructTreeRoot") is not None:
            return True
        else:
            return False
    if isinstance(document, Pdf):
        if document.Root.get("/StructTreeRoot") is not None:
            return True
        else:
            return False


def check_for_alt_tags(document):

    root = document.Root.get("/StructTreeRoot")
    roleMap = root.get("/RoleMap")
    document_photos = list()
    IDDict = {}






    if not check_if_tagged(document):
        raise Exception("PDF Not Tagged")
    # print(repr(document.Root.get("/Names")))


    def recurse_a_node(node, parent):

        if isinstance(node, Dictionary):


            if "/BBox" in node.keys():

                if "/Pg" in parent.keys():
                    global BboxCount
                    BboxCount += 1
                    if '/Alt' in parent.keys():
                        document_photos.append(True)
                    else:
                        document_photos.append(False)
            if '/K' in node.keys():
                recurse_k_nodes(node)

        if isinstance(node, Array):

            for each in node:
                recurse_a_node(each, parent)

    def recurse_s_node(node):
        global images

        def check_xObject():

            def check_xObject_image(iXobject):

                if iXobject.get("/Subtype") == "/Image":

                    image_bytes = iXobject.get_raw_stream_buffer()
                    hasher = hashlib.md5()
                    hasher.update(image_bytes)
                    image_hash = hasher.hexdigest()


                    derived_id = iXobject.get("/Height") + iXobject.get("/Width") + iXobject.get("/Length")  # uniqish id for dict

                    if "/Alt" in node.keys() and len(str(node.get('/Alt'))) > 0:

                        IDDict[image_hash] = True
                    else:
                        if derived_id in IDDict and IDDict[image_hash] is True:
                            IDDict[image_hash] = True
                        else:
                            IDDict[image_hash] = False
            try:
                resources = node.get('/Pg').get("/Resources")

                if "/XObject" in resources.keys():
                    XObject = resources.get("/XObject")
                    for key in XObject.keys():
                        if re.match(re.compile("/Fm\d|/P\d"), key):  # form Xobject?
                            fxobject_resources = XObject[key].get("/Resources")
                            if "/XObject" in fxobject_resources.keys():
                                for xobject_key in fxobject_resources["/XObject"]:
                                    if re.match(re.compile("/Im\d"), xobject_key):  # image Xobject?
                                        check_xObject_image(fxobject_resources["/XObject"][xobject_key])

                        else:
                            # print(repr(XObject))
                            check_xObject_image(XObject[key])

            except AttributeError:
                print(repr(node.get('/Pg')))

        if roleMap is not None and len(roleMap.keys()) > 0:
            try:
                if roleMap[node.get('/S')] == Name("/Figure"):
                    check_xObject()
            except KeyError:
                if node.get('/S') == Name("/Figure"):
                    check_xObject()
        else:
            if node.get('/S') == Name("/Figure"):
                check_xObject()

    def recurse_k_nodes(node):

        if isinstance(node, Dictionary):
            if "/K" in node.keys():
                recurse_k_nodes(node.get('/K'))
            # if "/A" in node.keys():
            #     recurse_a_node(node.get("/A"), node)
            if "/S" in node.keys():
                recurse_s_node(node)

        if isinstance(node, Array):
            for each in node:
                if isinstance(each, Dictionary):
                    # print((each.keys()))
                    if "/K" in each.keys():
                        recurse_k_nodes(each.get("/K"))

                    # if "/A" in each.keys():
                    #     recurse_a_node(each.get("/A"), each)

                    if "/S" in each.keys():
                        recurse_s_node(each)

                if isinstance(each, Array):
                    recurse_k_nodes(each)

    recurse_k_nodes(root)

    for figure in IDDict:
        document_photos.append(IDDict[figure])

    return document_photos


def verify_headings(document):

    root = document.Root.get("/StructTreeRoot")

    headings = []

    headings_map = {
        pikepdf.Name("/H1"): 1,
        pikepdf.Name("/H2"): 2,
        pikepdf.Name("/H3"): 3,
        pikepdf.Name("/H4"): 4,
        pikepdf.Name("/H5"): 5,
        pikepdf.Name("/H6"): 6,

    }

    def recurse_k_nodes(node):

        if isinstance(node, Dictionary):
            if "/K" in node.keys():
                recurse_k_nodes(node.get('/K'))
                if "/S" in node.keys():
                    if node.get("/S") in headings_map.keys():
                        headings.append(headings_map[node.get("/S")])


        if isinstance(node, Array):
            for each in node:
                if isinstance(each, Dictionary):
                    if "/K" in each.keys():
                        recurse_k_nodes(each.get("/K"))
                    if "/S" in each.keys():
                        if each.get("/S") in headings_map.keys():

                            headings.append(headings_map[each.get("/S")])

                if isinstance(each, Array):
                    recurse_k_nodes(each)

    recurse_k_nodes(root)

    # Matterhorn 14-001, 14-002, 14-003
    print("Headings Map", headings)
    if len(headings) == 0:
        return False

    if len(list(filter(lambda n: n == 1, headings))) > 1:  # greater than 1 H1 heading
        return False

    if len(headings) > 0:
        if headings[0] != 1:
            return False

    for i, h in enumerate(headings):
        if i + 1 == len(headings):
            break
        if (headings[i + 1] - h) > 1:
            return False

    return True



def check_metadata(document):

    meta = {
        "title": False,
        "language": False,
    }

    metadata = document.open_metadata()
    if isinstance(document.Root.get("/Lang"), Object):
        meta['language'] = True
    if metadata.get("dc:title"):
        meta['title'] = True
    return meta


def get_doc_data(document):

    doc_data = {
        "pages":len(document.pages)
    }
    return doc_data


def check_bookmarks(document):
    if check_if_tagged(document):
        outlines = document.Root.get("/Outlines")
        # print(repr(outlines))
        if outlines:
            if outlines.get("/Count"):
                if outlines.get("/Count") > 0:
                    return True
                else:
                    return False
            else:
                if outlines.get("/First"):
                    return True
                else:
                    return False
        else:
            return False
    else:
        return False


def pdf_check(location):

    try:
        Pikepdf = Pdf.open(location, allow_overwriting_input=True)
        tagged = check_if_tagged(Pikepdf)
        if tagged:
            alt_tag_count = check_for_alt_tags(Pikepdf)
        else:
            alt_tag_count = []
        pdf_text_type = pdf_status(location)

        obj = {

            "tagged": bool(tagged),
            "alt_tag_count": alt_tag_count,
            "pdf_text_type": pdf_text_type,
            "metadata": check_metadata(Pikepdf),
            "doc_data": get_doc_data(Pikepdf),
            "headings_pass": verify_headings(Pikepdf),
            "has_bookmarks": check_bookmarks(Pikepdf)

        }
    except PdfError as e:
        print("PDF READ ERROR", e)
        return None

    try:
        # Pikepdf.save()
        Pikepdf.close()
        return obj
    except PdfError as e:
        print("PDF WRITE ERROR", e)
        return None



print(pdf_check("Z:\ACRS\project_files\eeba80eee44994f0fed10fd9298a8c424f7c7875962a80014b72c52b10f26f9a\source\Distribution of Practice (slides only).pdf"))

#
# print(pdf_check(r"Z:\ACRS\project_files\47809652311603305dc42a9501a8267c6ec41b8e665de4f0d1a42d4a1d9d0440\active\2007_Book Reviews.pdf"))

# print(pdf_check(r"Z:\ACRS\project_files\3ffb2bf96f546d787e7e2c79ef4b81882ab05baf5ced7f31987e434c5125a889\active\2007_Donna DiGiuseppe.pdf"))

#
# add_bookmarks_from_headings(Pdf.open((r"Z:\ACRS\project_files\c0cb15bb4e996f17b129c54bd471b73c98b7b8a84b81f42c4aa8e01267a5981a\active\Desi Land California Here We Come .pdf")))


# add_bookmarks_from_headings(Pdf.open(r"Z:\ACRS\project_files\3ea4787285280c99a204416fe8204e6423607115ec5ab22632cd516349f73c76\active\Malcolm_Mafi_Crisis.pdf"))



# print(pdf_check(r"Z:\ACRS\project_files\ae37b2abbe4bd48244c604f602464fdca6563f8c6378e53e27430d55b8638fd5\source\EDD 786-07 Sp22 Syllabus.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\1f2b9c41f10c0dcbc69ffe9adc6c03ee55bba87c70fe687213c4ebccb56284ff\source\Blooms Taxonomy for Teaching Lesson Design.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\8b8999c25661c10085d0ababe7050af301ebc78f9dbb03edeeab187db0424aca\source\EdTPA Making Good Choices 21-22.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\fdf547da4d49ff8410276d99cbece4cd9b6afe2dd5f2636bcb7dd2357f933e1b\source\Ladder-of-Inference-Overview.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\958ec82c340f47c94c8788e4adbbcebf74a3fb160b94f312b0fc09ef8540bafe\active\Ethnic mobilization among Korean dry cleaners (1).pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\3ffb2bf96f546d787e7e2c79ef4b81882ab05baf5ced7f31987e434c5125a889\active\2007_Donna DiGiuseppe.pdf"))