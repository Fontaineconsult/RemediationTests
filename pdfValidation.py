import pikepdf
from pdfminer import high_level
from pdfminer.layout import LTImage
import pdfminer
from pikepdf import Pdf, Dictionary, Array, String, Object, Name, PdfError, OutlineItem
import re



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

        def check_xObject():

            resources = node.get('/Pg').get("/Resources")
            if "/XObject" in resources.keys():
                XObject = resources.get("/XObject")

                for key in XObject.keys():
                    if XObject[key].get("/Subtype") == "/Image":
                        derived_id = XObject[key].get("/Height") + XObject[key].get("/Width") + XObject[key].get("/Length")
                        IDDict[derived_id] = [key]

                        if "/Alt" in node.keys() and len(str(node.get('/Alt'))) > 0:
                            IDDict[derived_id] = True
                        else:
                            IDDict[derived_id] = False

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
            if "/A" in node.keys():
                recurse_a_node(node.get("/A"), node)
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



def normalize_headings(document):

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

    def find_group(start_index):
        pass

    def recurse_k_nodes(node):

            if isinstance(node, Dictionary):
                if "/K" in node.keys():
                    recurse_k_nodes(node.get('/K'))
            if isinstance(node, Array):
                for each in node:
                    if isinstance(each, Dictionary):
                        if "/K" in each.keys():
                            recurse_k_nodes(each.get("/K"))
                        if "/S" in each.keys():

                            if each.get("/S") in headings_map.keys():

                                if len(headings) == 0:
                                    if each.get("/S") != "/H1":
                                        each["/S"] = Name("/H1")
                                        headings.append(headings_map[each.get("/S")])

                                else:

                                    if len(headings) == 1:
                                        print(headings)
                                        if headings_map[each.get("/S")] - headings[0] > 1:
                                            each["/S"] = headings[0] + 1
                                            headings.append(each["/S"])
                                    else:
                                        if headings_map[each.get("/S")] - headings[-1] > 1:
                                            each["/S"] = headings[-1] + 1
                                            headings.append(each["/S"])

                    if isinstance(each, Array):
                        recurse_k_nodes(each)


    recurse_k_nodes(root)
    print(headings)

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


def add_bookmarks_from_headings(Pikepdf):

    root = Pikepdf.Root.get("/StructTreeRoot")
    parent_tree = root.get("/ParentTree")
    # print(repr(Pikepdf.Root))
    def recurse_k_nodes(node):

        if isinstance(node, Dictionary):
            if "/K" in node.keys():

                recurse_k_nodes(node.get('/K'))
        if isinstance(node, Array):

            for each in node:

                if isinstance(each, Dictionary):
                    if "/K" in each.keys():

                        recurse_k_nodes(each.get("/K"))

                    if "/S" in each.keys():

                        if each.get("/S") in ["/H1", "/H2", "/H3", "/H4", "/H5", "/H6"]:

                            # if each.get("/S") == "/H1":
                            #     print(repr(each.get('/Pg')))

                            mcid = each.get("/K")

                            page_bytes = each.get('/Pg').get("/Contents").read_bytes()
                            # print(page_bytes)
                            # Get Bookmark Position
                            raw_location_re = f"<</MCID {mcid} >>BDC\s(.*?)(Tm|Td)"
                            mcid_re = re.compile(raw_location_re, flags=re.DOTALL)
                            location_string = re.search(mcid_re, page_bytes.decode('utf-8'))
                            if location_string is not None:
                                x = location_string.group().split()[-3]
                                y = location_string.group().split()[-2]
                            else:
                                print("Failed to find bookmark data")
                                continue

                            # Get Bookmark Title
                            raw_title_re = f"<</MCID {mcid} >>BDC(.*?)EMC"
                            title_re = re.compile(raw_title_re, flags=re.DOTALL)
                            title_string = re.search(title_re, page_bytes.decode('utf-8'))
                            in_paren = False
                            output = []
                            for position, char in enumerate(title_string.group()):
                                if char == "(":
                                    in_paren = True
                                    continue
                                if char == ")":
                                    in_paren = False
                                    continue
                                if in_paren is True:
                                    output.append(char)
                            bookmark_title = "".join(output)
                            page_number = _get_page_number_of_page(each.get("/Pg"), Pikepdf)

                            with Pikepdf.open_outline() as outline:
                                oi = OutlineItem(bookmark_title, page_number - 1, "XYZ", left=int(float(x)),
                                                 top=int(float(y)))
                                outline.root.append(oi)

                if isinstance(each, Array):
                    recurse_k_nodes(each)
    if Pikepdf.Root.get("/AcroForm"):
        if "/PDFDocEncoding" in Pikepdf.Root.AcroForm.DR.Encoding.keys():
            if isinstance(Pikepdf.Root.Pages.Kids, Array):
                print("Adding Bookmarks")
                recurse_k_nodes(parent_tree.get("/Nums"))
            else:
                print("Page stored as Dict")
        else:
            print("Encoding Not Supported for Bookmarks")
    else:
        recurse_k_nodes(parent_tree.get("/Nums"))

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



def repair_pdf(location):

    try:
        Pikepdf = Pdf.open(location, allow_overwriting_input=True)
        normalize_headings(Pikepdf)


    except PdfError as e:
        print("PDF WRITE ERROR", e)
        return None




print(pdf_check(r"Z:\ACRS\project_files\3ffb2bf96f546d787e7e2c79ef4b81882ab05baf5ced7f31987e434c5125a889\active\2007_Donna DiGiuseppe.pdf"))
repair_pdf(r"Z:\ACRS\project_files\3ffb2bf96f546d787e7e2c79ef4b81882ab05baf5ced7f31987e434c5125a889\active\2007_Donna DiGiuseppe.pdf")
#
# add_bookmarks_from_headings(Pdf.open((r"Z:\ACRS\project_files\c0cb15bb4e996f17b129c54bd471b73c98b7b8a84b81f42c4aa8e01267a5981a\active\Desi Land California Here We Come .pdf")))


# add_bookmarks_from_headings(Pdf.open(r"Z:\ACRS\project_files\3ea4787285280c99a204416fe8204e6423607115ec5ab22632cd516349f73c76\active\Malcolm_Mafi_Crisis.pdf"))



# print(pdf_check(r"Z:\ACRS\project_files\ae37b2abbe4bd48244c604f602464fdca6563f8c6378e53e27430d55b8638fd5\source\EDD 786-07 Sp22 Syllabus.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\1f2b9c41f10c0dcbc69ffe9adc6c03ee55bba87c70fe687213c4ebccb56284ff\source\Blooms Taxonomy for Teaching Lesson Design.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\8b8999c25661c10085d0ababe7050af301ebc78f9dbb03edeeab187db0424aca\source\EdTPA Making Good Choices 21-22.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\fdf547da4d49ff8410276d99cbece4cd9b6afe2dd5f2636bcb7dd2357f933e1b\source\Ladder-of-Inference-Overview.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\958ec82c340f47c94c8788e4adbbcebf74a3fb160b94f312b0fc09ef8540bafe\active\Ethnic mobilization among Korean dry cleaners (1).pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\3ffb2bf96f546d787e7e2c79ef4b81882ab05baf5ced7f31987e434c5125a889\active\2007_Donna DiGiuseppe.pdf"))