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
    document_photos = list()
    if not check_if_tagged(document):
        raise Exception("PDF Not Tagged")
    print(repr(root))
    def recurse(node):

        if isinstance(node, Dictionary):
            if '/K' in node.keys():
                next_node = node.get('/K')
                recurse(next_node)
            if '/A' in node.keys():
                next_node = node.get('/A')
                recurse(next_node)
        if isinstance(node, Array):
            for item in node:
                if isinstance(item, Dictionary):
                    print("DICTIONARY")
                if isinstance(item, Array):
                    print("Arrayyyy")


                if isinstance(item, Dictionary):

                    # if '/Alt' in item.keys():
                    #     if '/S' in item.keys():
                    #         print(repr(item.get("/S")))
                    #         print(repr(item.get("/Pg")))

                    if "/A" in item.keys():
                        try:
                            if '/BBox' in item.get('/A'):
                                if '/Alt' in item.keys():
                                    document_photos.append(True)
                                else:
                                    document_photos.append(False)

                        except TypeError:
                            if String('/BBox') in item.get('/A'):
                                if '/Alt' in item.keys():
                                    document_photos.append(True)
                                else:
                                    document_photos.append(False)

                    if "/K" in item.keys():
                        next_node = item.get('/K')
                        recurse(next_node)

                if isinstance(item, Array):

                    print("___________ array in array")
                    recurse(item)


    recurse(root)
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

        "tagged": tagged,
        "alt_tag_count": alt_tag_count,
        "pdf_text_type": pdf_text_type,
        "metadata": check_metadata(Pikepdf)

    }
    return obj


# print(pdf_check(r"Z:\ACRS\project_files\ae37b2abbe4bd48244c604f602464fdca6563f8c6378e53e27430d55b8638fd5\source\EDD 786-07 Sp22 Syllabus.pdf"))
print(pdf_check(r"Z:\ACRS\project_files\1f2b9c41f10c0dcbc69ffe9adc6c03ee55bba87c70fe687213c4ebccb56284ff\source\Blooms Taxonomy for Teaching Lesson Design.pdf"))