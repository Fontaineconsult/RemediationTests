from pdfminer import high_level
import pdfminer
from pikepdf import Pdf, Dictionary, Array



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
            variance = (item.x1 * item.y1) / (page.x1 * page.y1)
            if 0.9 < variance < 1.1:  # Check to see if the size of the text image is the same as the page
                return True
            else:
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

    pdf = Pdf.open(document)
    root = pdf.Root.get("/StructTreeRoot")
    document_photos = list()
    print(repr(pdf.Root))

    if not check_if_tagged(pdf):
        raise Exception("PDF Not Tagged")

    def recurse(node):

        if isinstance(node, Dictionary):
            print(node.keys())
            if '/K' in node.keys():
                next_node = node.get('/K')
                recurse(next_node)
        if isinstance(node, Array):
            for item in node:
                if isinstance(item, Dictionary):
                    print(item.keys())
                    if "/A" in item.keys():
                        if '/BBox' in item.get('/A'):
                            if '/Alt' in item.keys():
                                document_photos.append(True)
                            else:
                                document_photos.append(False)

                    if "/K" in item.keys():
                        next_node = item.get('/K')
                        recurse(next_node)


    recurse(root)
    return document_photos





