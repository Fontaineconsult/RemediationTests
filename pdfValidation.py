from pdfminer import high_level
import pdfminer
from pikepdf import Pdf, Dictionary, Array, String, Object, Name



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
                    print((each.keys()))
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





# check_metadata(r"Z:\ACRS\Requests\E_ED 0786-07\Math Resources\Learning About Rulers and Measuring.pdf")
# check_metadata(r"Z:\ACRS\Requests\E_ED 0786-07\Math Resources\Learning Geometry-  Some Insights Drawn from Teacher Writing.pdf")


def pdf_check(location):

    Pikepdf = Pdf.open(location)

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

    }
    return obj


# print(pdf_check(r"Z:\ACRS\project_files\ae37b2abbe4bd48244c604f602464fdca6563f8c6378e53e27430d55b8638fd5\source\EDD 786-07 Sp22 Syllabus.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\1f2b9c41f10c0dcbc69ffe9adc6c03ee55bba87c70fe687213c4ebccb56284ff\source\Blooms Taxonomy for Teaching Lesson Design.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\8b8999c25661c10085d0ababe7050af301ebc78f9dbb03edeeab187db0424aca\source\EdTPA Making Good Choices 21-22.pdf"))
# print(pdf_check(r"Z:\ACRS\project_files\fdf547da4d49ff8410276d99cbece4cd9b6afe2dd5f2636bcb7dd2357f933e1b\source\Ladder-of-Inference-Overview.pdf"))